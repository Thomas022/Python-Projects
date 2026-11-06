// Shared table feedback and local-file answer saving for Lessons 19 onward.
document.querySelectorAll('[data-lesson-results]').forEach(form => {
  const lesson = Number(form.dataset.lessonResults);
  const fields = [...form.querySelectorAll('select, textarea[name="reason"]')];
  const feedback = form.querySelector('[role="status"]');
  let lessonFile;
  try {
    const saved = JSON.parse(document.getElementById('saved-lesson-answers').textContent);
    if (saved.lesson === lesson && saved.responses) {
      fields.forEach(field => {
        const value = saved.responses[field.name];
        if (typeof value === 'string' &&
            (field.tagName !== 'SELECT' || [...field.options].some(option => option.value === value))) {
          field.value = value;
        }
      });
    }
  } catch { feedback.textContent = 'Saved answers could not be loaded; enter them below.'; }
  form.addEventListener('submit', event => {
    event.preventDefault();
    const choices = fields.filter(field => field.tagName === 'SELECT');
    let correct = 0;
    choices.forEach(field => {
      const ok = field.value === field.dataset.correct;
      correct += Number(ok);
      field.setAttribute('aria-invalid', String(!ok));
      field.nextElementSibling.textContent = ok ? 'Correct' : 'Review this value.';
    });
    feedback.textContent = `${correct}/${choices.length} entries correct. Your explanation is for discussion with your teacher.`;
  });
  function resultsText() {
    const lines = [form.dataset.heading];
    form.querySelectorAll('tbody tr').forEach(row => {
      lines.push([row.querySelector('th').textContent,
        ...[...row.querySelectorAll('select')].map(field => field.value || '__')].join(' | '));
    });
    lines.push('', `${form.querySelector('label[for="reason"]').textContent} ${form.elements.namedItem('reason').value.trim() || '__'}`);
    return lines.join('\n');
  }
  form.querySelector('[data-copy-results]').addEventListener('click', async () => {
    const text = resultsText();
    try { await navigator.clipboard.writeText(text); feedback.textContent = 'Copied. Paste into chat.'; }
    catch {
      const output = form.querySelector('[data-results-export]');
      output.hidden = false; output.value = text; output.focus(); output.select();
      feedback.textContent = 'Copy the selected text below.';
    }
  });
  form.querySelector('[data-save-results]').addEventListener('click', async () => {
    if (typeof window.showOpenFilePicker !== 'function') {
      feedback.textContent = 'Use Chrome or Edge to save into the lesson file, or copy your results for chat.';
      return;
    }
    const button = form.querySelector('[data-save-results]');
    button.disabled = true;
    try {
      if (!lessonFile) [lessonFile] = await window.showOpenFilePicker({multiple: false,
        types: [{description: 'Lesson HTML', accept: {'text/html': ['.html']}}]});
      const source = await (await lessonFile.getFile()).text();
      const marker = /<script type="application\/json" id="saved-lesson-answers">[\s\S]*?<\/script>/g;
      if (!source.includes(`data-lesson-results="${lesson}"`) || (source.match(marker) || []).length !== 1) {
        throw new Error(`Choose the original Lesson ${lesson} HTML file.`);
      }
      const saved = {lesson, savedAt: new Date().toISOString(),
        responses: Object.fromEntries(fields.map(field => [field.name, field.value]))};
      const json = JSON.stringify(saved, null, 2).replace(/</g, '\\u003c');
      const updated = source.replace(marker, () => `<script type="application/json" id="saved-lesson-answers">${json}</script>`);
      const writable = await lessonFile.createWritable();
      await writable.write(updated); await writable.close();
      feedback.textContent = 'Answers saved inside this lesson. Save again after editing.';
    } catch (error) {
      lessonFile = undefined;
      feedback.textContent = error.name === 'AbortError' ? 'Save canceled; entries remain on this page.' : error.message;
    } finally { button.disabled = false; }
  });
});

// Keep saved responses inert and readable in the lesson source.
function embedLessonAnswers(source, answers) {
  const marker = /<script type="application\/json" id="saved-lesson-answers">[\s\S]*?<\/script>/g;
  if ((source.match(marker) || []).length !== 1 || !source.includes('data-lesson-id="14"')) {
    throw new Error('Choose the original Lesson 14 HTML file.');
  }
  const json = JSON.stringify(answers, null, 2).replace(/</g, '\\u003c');
  return source.replace(marker, () => `<script type="application/json" id="saved-lesson-answers">${json}</script>`);
}

document.querySelectorAll('[data-results-table]').forEach(form => {
  const expected = {
    good: {retrievals: '2', generations: '1', price: '$5', node: 'release'},
    repair: {retrievals: '2', generations: '2', price: '$5', node: 'release'},
    stuck: {retrievals: '2', generations: '2', price: '$50', node: 'reject_answer'}
  };
  const feedback = form.querySelector('[data-results-feedback]');
  const fields = [...form.querySelectorAll('select')];
  let lessonFile;
  try {
    const saved = JSON.parse(document.getElementById('saved-lesson-answers').textContent);
    if (saved.lesson === 14 && saved.responses) {
      [...fields, form.elements.namedItem('reason')].forEach(field => {
        const value = saved.responses[field.name];
        if (typeof value === 'string' && (field.tagName !== 'SELECT' || [...field.options].some(option => option.value === value))) {
          field.value = value;
        }
      });
      feedback.textContent = 'Your saved answers are loaded. Edit them and save again when ready.';
    }
  } catch {
    feedback.textContent = 'Saved answers could not be loaded. You can enter and save new answers.';
  }
  form.addEventListener('submit', event => {
    event.preventDefault();
    let correct = 0;
    let missing = 0;
    fields.forEach(field => {
      const [mode, key] = field.name.split('-');
      const valid = field.value === expected[mode][key];
      if (valid) correct++;
      if (!field.value) missing++;
      field.setAttribute('aria-invalid', String(!valid));
      field.nextElementSibling.textContent = !field.value ? 'Choose a value.' : valid ? 'Correct' : 'Review this value.';
    });
    feedback.textContent = correct === fields.length
      ? 'All 12 table entries are correct. Save your answers or copy them to share your explanation.'
      : `${correct} of 12 entries correct.${missing ? ` ${missing} still need a value.` : ''} Review the marked cells and the run summaries.`;
  });
  form.addEventListener('change', event => {
    if (!event.target.matches('select')) return;
    event.target.removeAttribute('aria-invalid');
    event.target.nextElementSibling.textContent = '';
    feedback.textContent = 'Selection updated. Check the table again when ready.';
  });
  function resultsText() {
    const lines = ['Mode | Retrievals | Generations | Final draft price | Final node'];
    Object.keys(expected).forEach(mode => {
      lines.push([mode, ...Object.keys(expected[mode]).map(key => form.elements.namedItem(`${mode}-${key}`).value || '__')].join(' | '));
    });
    lines.push('', `What does repair_feedback add? ${form.elements.namedItem('reason').value.trim() || '__'}`);
    return lines.join('\n');
  }
  form.querySelector('[data-copy-results]').addEventListener('click', async () => {
    const text = resultsText();
    try {
      await navigator.clipboard.writeText(text);
      feedback.textContent = 'Results copied. Paste them into chat.';
    } catch {
      const output = form.querySelector('[data-results-export]');
      output.value = text;
      output.hidden = false;
      form.querySelector('[data-copy-help]').hidden = false;
      output.focus();
      output.select();
      feedback.textContent = 'Automatic copying is unavailable. The results below are selected; copy them manually.';
    }
  });
  form.querySelector('[data-save-results]').addEventListener('click', async () => {
    if (typeof window.showOpenFilePicker !== 'function') {
      feedback.textContent = 'Saving into HTML is unavailable in this browser. Open this lesson in Chrome or Edge and try again, or use Copy results for chat.';
      return;
    }
    const button = form.querySelector('[data-save-results]');
    button.disabled = true;
    try {
      if (!lessonFile) {
        [lessonFile] = await window.showOpenFilePicker({
          multiple: false,
          types: [{description: 'Lesson HTML', accept: {'text/html': ['.html']}}]
        });
      }
      const responses = Object.fromEntries([...fields, form.elements.namedItem('reason')].map(field => [field.name, field.value]));
      const source = await (await lessonFile.getFile()).text();
      const updated = embedLessonAnswers(source, {lesson: 14, savedAt: new Date().toISOString(), responses});
      const writable = await lessonFile.createWritable();
      await writable.write(updated);
      await writable.close();
      feedback.textContent = 'Answers saved inside the lesson HTML. You can now ask: “Check my Lesson 14 answers.” Save again after editing.';
    } catch (error) {
      lessonFile = undefined;
      feedback.textContent = error.name === 'AbortError'
        ? 'Save canceled. Your entries are still on this page.'
        : `Answers were not saved. ${error.message || 'Check file access and try again.'}`;
    } finally {
      button.disabled = false;
    }
  });
});

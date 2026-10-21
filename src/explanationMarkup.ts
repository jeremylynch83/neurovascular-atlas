import content from './explanationContent.json' with { type: 'json' };

function escape(text: string): string {
  return text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}
export const explanationSummary = content.summary;
export function explanationSectionsMarkup(level: 2 | 3 = 2): string {
  return content.sections.map(section => {
    const paragraph = section.paragraph.map(part => {
      let text = escape(part.text);
      if ('italic' in part && part.italic) text = `<em>${text}</em>`;
      if ('href' in part && part.href) {
        if (!part.href.startsWith('https://')) throw new Error('Explanation links must use HTTPS');
        text = `<a href="${escape(part.href)}" target="_blank" rel="noopener noreferrer">${text}</a>`;
      }
      return text;
    }).join('');
    return `<h${level}>${escape(section.heading)}</h${level}><p>${paragraph}</p>`;
  }).join('');
}
export function explanationMarkup(): string {
  return `<p>${escape(explanationSummary)}</p>${explanationSectionsMarkup()}`;
}

import type { ReactNode } from 'react';
import type { Structure } from './types';

export function Description({ text, byId, onSelect }: {
  text: string;
  byId: ReadonlyMap<string, Structure>;
  onSelect: (structure: Structure) => void;
}) {
  const paragraph = (text: string): ReactNode[] => {
    const parts: ReactNode[] = [];
    const links = /\[([^\]]+)\]\(#structure-([^\)]+)\)/g;
    let offset = 0;
    for (const match of text.matchAll(links)) {
      parts.push(text.slice(offset, match.index));
      const target = byId.get(match[2]);
      parts.push(target ? <a key={match.index} href={`#structure-${target.id}`} onClick={event => {
        event.preventDefault();
        onSelect(target);
      }}>{match[1]}</a> : match[1]);
      offset = match.index + match[0].length;
    }
    parts.push(text.slice(offset));
    return parts;
  };

  return <section className="structure-description">
    <h3>Description</h3>
    {text.trim().split(/\n\s*\n/).map((text, index) => <p key={index}>{paragraph(text)}</p>)}
  </section>;
}

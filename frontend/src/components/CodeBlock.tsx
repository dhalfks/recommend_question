import { useMemo, useState } from 'react';

type CodeBlockProps = {
  code: string;
  language?: string | null;
  label?: string;
};

const extensionLanguages: Record<string, string> = {
  c: 'C',
  cpp: 'C++',
  cs: 'C#',
  css: 'CSS',
  go: 'Go',
  html: 'HTML',
  java: 'Java',
  js: 'JavaScript',
  json: 'JSON',
  jsx: 'JSX',
  kt: 'Kotlin',
  md: 'Markdown',
  php: 'PHP',
  py: 'Python',
  rb: 'Ruby',
  rs: 'Rust',
  sql: 'SQL',
  swift: 'Swift',
  ts: 'TypeScript',
  tsx: 'TSX',
  txt: 'Plain text',
  xml: 'XML',
  yaml: 'YAML',
  yml: 'YAML',
};

function languageName(value: string | null | undefined, code: string): string {
  if (!value) {
    if (/\b(SELECT|INSERT|UPDATE|DELETE|CREATE TABLE)\b/i.test(code)) return 'SQL';
    if (/\b(public static void main|System\.out\.print)/.test(code)) return 'Java';
    if (/\b(def |import |print\()/.test(code)) return 'Python';
    if (/\b(const|let|function|console\.log)\b/.test(code)) return 'JavaScript';
    return 'Code';
  }
  const normalized = value.split('?')[0].split('.').pop()?.toLowerCase() ?? value;
  return extensionLanguages[normalized] ?? languageName(undefined, code);
}

export default function CodeBlock({ code, language, label }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);
  const lines = useMemo(() => code.replace(/\r\n/g, '\n').split('\n'), [code]);

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  };

  return (
    <figure className="mb-5 overflow-hidden rounded-xl border border-slate-700 bg-[#242C34] shadow-sm">
      <figcaption className="flex items-center justify-between border-b border-white/10 bg-black/15 px-4 py-2 text-xs text-slate-300">
        <span className="flex items-center gap-2">
          <span aria-hidden="true" className="text-slate-400">&lt;/&gt;</span>
          {label && <strong className="font-medium text-slate-100">{label}</strong>}
          <span>{languageName(language, code)}</span>
        </span>
        <button
          type="button"
          onClick={copyCode}
          className="rounded-md px-2 py-1 transition hover:bg-white/10 hover:text-white"
          aria-label="소스 코드 복사"
        >
          {copied ? '복사됨' : '복사'}
        </button>
      </figcaption>
      <pre className="overflow-x-auto py-4 text-sm leading-6 text-slate-100">
        <code>
          {lines.map((line, index) => (
            <span key={index} className="block min-w-max px-4">
              <span
                aria-hidden="true"
                className="mr-5 inline-block w-7 select-none text-right text-slate-500"
              >
                {index + 1}
              </span>
              <span>{line || ' '}</span>
            </span>
          ))}
        </code>
      </pre>
    </figure>
  );
}

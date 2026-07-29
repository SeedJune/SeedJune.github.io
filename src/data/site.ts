/* ==========================================================================
   Everything on this site that is a short, image-free list lives here.
   Anything with a picture or a body of prose lives in src/content/ instead.

   Fields marked TODO are placeholders — replace the string, keep the shape.
   To remove an entry, delete its object. To add one, copy an existing object.
   An empty array renders as a quiet "nothing here yet" note, not a broken
   section, so it is safe to leave any of these empty.
   ========================================================================== */

export const profile = {
  name: 'Yuchao Jin',
  pronouns: 'he/him',
  role: 'TODO: e.g. Undergraduate',
  affiliation: 'TODO: e.g. School of EECS, Peking University',
  affiliationUrl: 'https://eecs.pku.edu.cn/',
  /* One or two sentences. Shown at the top of the About section. */
  tagline: 'TODO: one line — what you work on, in plain words.',
  /* The longer intro. Two to four sentences reads best. */
  bio: 'TODO: a short paragraph about who you are, what you study, and what you are interested in right now. Two to four sentences is the sweet spot.',
  interests: [
    'TODO: research interest 1',
    'TODO: research interest 2',
    'TODO: research interest 3',
  ],
} as const;

/* Shown as a short text list in the sidebar. Delete any line you do not want.
   Order here is the order on screen. */
export const socials: { label: string; href: string }[] = [
  { label: 'Email', href: 'mailto:yuchaojin99@gmail.com' },
  { label: 'GitHub', href: 'https://github.com/SeedJune' },
  { label: 'CSDN', href: 'TODO: your CSDN profile URL' },
  { label: 'RedNote', href: 'TODO: your Xiaohongshu profile URL' },
];

/* Short dated updates. Newest first. Keep each to one sentence.
   Leave the array empty until you have something to announce. */
export const news: { date: string; text: string }[] = [
  // { date: '2026-07', text: 'Started my graduate studies at ...' },
];

export const education: {
  degree: string;
  org: string;
  start: string;
  end: string | null;
  current?: boolean;
  summary?: string;
}[] = [
  {
    degree: 'TODO: degree and major',
    org: 'TODO: school or department',
    start: 'YYYY-MM',
    end: null,
    current: true,
  },
];

export const experience: {
  role: string;
  org: string;
  start: string;
  end: string | null;
  current?: boolean;
  summary?: string;
}[] = [
  {
    role: 'TODO: your role',
    org: 'TODO: lab, company, or program',
    start: 'YYYY-MM',
    end: 'YYYY-MM',
    summary: 'TODO: one or two sentences on what you actually did.',
  },
];

export const awards: { title: string; org: string; date: string }[] = [
  {
    title: 'TODO: award name',
    org: 'TODO: awarding body',
    date: 'YYYY-MM',
  },
];

export const skills = {
  technical: ['TODO: language or tool', 'TODO: language or tool'],
  languages: [
    { name: 'TODO: language', level: 'TODO: e.g. Native' },
    { name: 'TODO: language', level: 'TODO: e.g. Professional working' },
  ],
  /* Hobbies render in pink — the personal axis. Emoji are welcome here. */
  hobbies: ['TODO: hobby', 'TODO: hobby'],
};

/* Used for <title>, meta description, Open Graph, and the sitemap. */
export const site = {
  url: 'https://seedjune.github.io',
  title: 'Yuchao Jin',
  description: 'TODO: one sentence describing you, for search results and link previews.',
  startYear: 2026,
} as const;

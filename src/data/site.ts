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
  role: 'Undergraduate Student',
  affiliation: 'School of Electronics Engineering and Computer Science, Peking University',
  affiliationUrl: 'https://eecs.pku.edu.cn/',
  /* One or two sentences. Shown at the top of the About section. */
  tagline: 'Recently, I work on Artificial Intelligence, especially in the field of 3D vision and spatial understanding. Meanwhile, I work hard to learn computer system(CSAPP) and RL(Westlake University Windy Lab) these days.',
  /* The longer intro. Two to four sentences reads best. */
  bio: `Hi there! I'm an undergraduate at Peking University, specifically within the School of EECS, where I major in Intelligent Science and Technology. I have a strong passion for Computer Vision, Multimodal LLMs, and Embodied AI. After exploring 3D Gaussian Splatting and reconstruction techniques, I have recently shifted my focus to spatial reasoning via the representation of 3DGS. I'm also fond of Embodied AI and trying to learn more about it, including hardwares and algorithms.
  I also take a minor in Economics during my undergraduate studies, among which I love macro-economics most. I enjoy the inference procedure that analizing the countries' political and enconomic policies via the classic models and theories during class.
  In my leisure, I like reading. The whodunits written by Agatha Christie and Keigo Higashino, the history books that discribes ancient Chinese and Europe are all my favorites.
  I'm always open to discussing ideas with like-minded people—feel free to reach out and connect!`,

  /* ------------------------------------------------------------------------
     Chinese version of `tagline` and `bio` above. The About section shows the
     English one and offers a toggle; nothing else on the site is translated.

     Both must be filled in for the toggle to appear — see About.astro. That
     way a half-finished translation can never ship as a button that switches
     the intro to a blank panel.
     ------------------------------------------------------------------------ */
  taglineZh:
    '最近我主要做人工智能方向的研究，具体是三维视觉与空间理解。同时也在认真补计算机系统和强化学习相关的课程。',
  bioZh: `你好！我是一名北京大学的本科生，就读于信息科学技术学院，主修智能科学与技术。我对计算机视觉、多模态大模型和具身智能有着浓厚的兴趣。在探索过 3D 高斯泼溅与三维重建技术之后，我最近把重心转向了基于 3DGS 表示的空间推理。我同样对具身智能感兴趣，也在学习更多相关的知识，包括硬件与算法。
  本科期间我还辅修了经济学，其中最喜欢的是宏观经济学。我很享受课堂上用经典模型和理论去推演各国政治与经济政策的那个过程。
  闲暇时我喜欢读书。阿加莎·克里斯蒂和东野圭吾的推理小说，以及讲述中国古代史与欧洲中世纪史的书，都是我的最爱。
  我很乐意和志同道合的朋友交流想法——欢迎随时联系我！`,
  interests: [
    '3D Vision',
    'Embodied AI',
    'Multimodal Learning',
  ],
} as const;

/* Shown as a short text list in the sidebar. Delete any line you do not want.
   Order here is the order on screen. */
/* `icon` picks the glyph drawn in front of the label — see SocialIcon.astro
   for the list it understands. It is optional: leave it off and the link gets
   a generic chain-link glyph, so adding a new social never breaks the row. */
export const socials: { label: string; href: string; icon?: string }[] = [
  { label: 'Email', href: 'mailto:yuchaojin99@gmail.com', icon: 'email' },
  { label: 'GitHub', href: 'https://github.com/SeedJune', icon: 'github' },
  { label: 'CSDN', href: 'https://blog.csdn.net/jycjn?type=blog', icon: 'csdn' },
  {
    label: 'RedNote',
    href: 'https://www.xiaohongshu.com/user/profile/6617f7ab00000000070064ca',
    icon: 'rednote',
  },
];

/* Short dated updates. Newest first. Keep each to one sentence.
   Leave the array empty until you have something to announce. */
export const news: { date: string; text: string }[] = [
  // { date: '2026-07', text: 'Started my graduate studies at ...' },
  {date: '2026-07', text: '🎉🎉🎉 Access the summer camp of School of Intelligence Science and Technology, Peking University.'},
  {date: '2026-08', text: '♟️♟️♟️ I release some board games bots, including chinese checkers and Othello games.'}
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
    degree: 'Undergraduate student',
    org: 'School of EECS, PKU',
    start: '2023-09',
    end: null,
    current: true,
  },
  {
    degree: 'Undergraduate student',
    org: 'National School of Development, PKU',
    start: '2024-09',
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
    role: 'Summer research project',
    org: 'Visual Computing and Learning Lab, PKU',
    start: '2025-07',
    end: '2025-08',
    summary: 'I made some researches on the intersection of 3D Gaussian Splatting, satellite image 3D Reconstruction and SDS Loss',
  },
];

export const awards: { title: string; org: string; date: string }[] = [
  {
    title: '"Jiang Zhehan Cup" Mathematical Modeling and Computer Application Competition - Second Prize',
    org: 'School of Mathematical Science, Peking University',
    date: '2025-04',
  },
  {
    title: 'Scholarship of Peking University',
    org: 'Peking University',
    date: '2025-12',
  },
];

export const skills = {
  technical: ['Python', 'C++', 'MuJoCo'],
  languages: [
    { name: 'Chinese', level: 'Native' },
    { name: 'English', level: 'Listening and reading' },
  ],
  /* Hobbies render in pink — the personal axis. Emoji are welcome here. */
  hobbies: ['⚽️Soccer', '🛼Skating', '📸Photography', '⛰️Hiking', '🎮Gaming'],
};

/* --------------------------------------------------------------------------
   Blog series — the filter tabs above the Blogs section, in this order.

   `id` is what a post's `series:` frontmatter field has to match. It is
   validated in src/content.config.ts against this exact list, so a typo in a
   post fails the build and names the file rather than quietly inventing a
   series nobody can click on.

   Renaming a series = change `label` here (cosmetic, nothing else to touch).
   Changing an `id` = you must update the `series:` line in every post that
   used it, or the build will tell you which ones you missed.

   A series with no published posts is skipped — no empty tab is rendered.
   -------------------------------------------------------------------------- */
export const blogSeries = [
  {id: '3dgs', label: 'Gaussian Splatting'},
  {id: 'world model', label: 'World Models'},
  {id: 'csapp', label: 'CSAPP Notes' },
  {id: 'books and movies', label: 'Books & Movies' },
  {id: 'math', label: 'Mathematics'},
  {id: 'algorithm', label: 'Algorithms'},
  {id: 'games', label: 'Games'},
  {id: 'economics', label: 'Economics'},
  {id: 'culture', label: 'Culture'},
  {id: 'other', label: 'Others' },
] as const;

/* Used for <title>, meta description, Open Graph, and the sitemap. */
export const site = {
  url: 'https://seedjune.github.io',
  title: 'Yuchao Jin',
  description: 'An undergraduate student major in artificial intelligence.',
  startYear: 2026,
} as const;

// @ts-check
/** @type {import('@vivliostyle/cli').VivliostyleConfigSchema} */
const vivliostyleConfig = {
  title: "{{ title }}",
  author: "{{ author }}",
  theme: '@vivliostyle/theme-techbook', // .css or local dir or npm package. default to undefined
  entry: [
    {
      path: 'contents.md',
      rel: 'contents',
    },
    "index.md"
  ],
};

module.exports = vivliostyleConfig;

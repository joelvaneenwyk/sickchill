
/** @type {import('ava').IConfig} */
const config = {
  require: ['ejs', '@babel/register', 'setup-browser-env'],
  files: [
    'contrib/setup-browser-env/test/*.test.mjs',
    '!contrib/setup-browser-env/test/fixtures/*.config.js',
    'tests/js/*.test.mjs',
  ],
  watchMode: {
    ignoreChanges: ['{dist,debian,coverage,docs,media,test-types,test-tap}/**'],
  },
};

export default config;

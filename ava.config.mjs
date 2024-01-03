const config = {
  require: ['ejs', '@babel/register', 'setup-browser-env'],
  files: [
    'tests/js/*.mjs',
    'tests/js/*.js',
    '!tests/**/{fixtures,helpers}/**',
  ],
  watchMode: {
    ignoreChanges: ['{dist,debian,coverage,docs,media,test-types,test-tap}/**'],
  },
};

export default config;

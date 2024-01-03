/**
 * Configuration for 'xo' linter.
 */

/** @type {import("xo").ESLintConfig} */
module.exports = {
  esnext: true,
  envs: [
    'browser',
  ],
  globals: [
    '_',
    'scRoot',
    'jQuery',
    '$',
    'metaToBool',
    'getMeta',
    'PNotify',
    'themeSpinner',
    'anonURL',
    'Gettext',
    'gt',
    '_n',
    'latinize',
  ],
  ignores: [
    '*.min.js',
    'dist/**/*',
    'sickchill/**/lib/*.js',
  ],
  rules: {
    'unicorn/filename-case': 'off',
    'unicorn/prefer-node-append': 'off',
    indent: [
      'error',
      2,
      {
        SwitchCase: 1,
      },
    ],
    'import/order': [
      'error',
      {
        alphabetize: {
          order: 'asc',
        },
        'newlines-between': 'always',
      },
    ],
    'import/newline-after-import': 'error',
    'unicorn/require-post-message-target-origin': 'off',
    'unicorn/prefer-event-target': 'off',
  },
  overrides: [
    {
      files: '**/*.d.*(c|m)ts',
      rules: {
        'import/extensions': 'off',
      },
    },
    {
      files: '**/browser-env.config.(c|m)(j|t)s',
      rules: {
        'unicorn/prefer-module': 'off',
      },
    },
    {
      files: 'test/**',
      rules: {
        'import/no-anonymous-default-export': 'off',
        'n/prefer-global/process': 'off',
      },
    },
    {
      files: 'test/**/fixtures/**',
      rules: {
        'n/file-extension-in-import': 'off',
      },
    },
  ],
};

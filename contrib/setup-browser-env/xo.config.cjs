/**
 * Configuration for 'xo' linter.
 */

/** @type {import("xo").ESLintConfig} */
module.exports = {
  space: 2,
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
      files: 'sickchill/gui/**/*.(c|m)(j|t)s',
      rules: {
        indent: [
          'error',
          4,
          {
            SwitchCase: 1,
          },
        ],
      },
    },
    {
      files: '**/(test|tests)/*.test.(c|m)(j|t)s',
      rules: {
        'import/no-anonymous-default-export': 'off',
      },
    },
    {
      files: '**/webpack.config.*',
      rules: {
        'n/prefer-global/process': 'off',
      },
    },
    {
      files: '**/browser-env.config.js',
      rules: {
        'unicorn/prefer-module': 'off',
      },
    },
  ],
};

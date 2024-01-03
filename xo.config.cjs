module.exports = {
    esnext: true,
    envs: [
        "browser"
    ],
    globals: [
        "_",
        "scRoot",
        "jQuery",
        "$",
        "metaToBool",
        "getMeta",
        "PNotify",
        "themeSpinner",
        "anonURL",
        "Gettext",
        "gt",
        "_n",
        "latinize"
    ],
    ignores: [
        "core.min.js",
        "vendor.min.js",
        "lib/**/*",
        "Gruntfile.js",
        "sickchill/gui/slick/js/lib/*",
        "frontend/static/*",
        "webpack.config.mjs"
    ],
    rules: {
        "unicorn/filename-case": "off",
        "unicorn/prefer-node-append": "off",
        'indent': 'off',
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
            files: 'examples/**',
            rules: {
                'ava/no-ignored-test-files': 'off',
                'ava/no-only-test': 'off',
                'unicorn/prefer-module': 'off',
            },
        },
        {
            files: [
                'test/**/fixtures/**',
                'test-tap/**fixture/**',
            ],
            rules: {
                'unicorn/no-empty-file': 'off',
            },
        },
        {
            files: 'test-types/**',
            rules: {
                'ava/assertion-arguments': 'off',
                'ava/no-ignored-test-files': 'off',
                'ava/no-skip-assert': 'off',
                'ava/use-t': 'off',
            },
        },
        {
            // TODO: Update tests.
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
        {
            // TODO: Update tests.
            files: 'test/snapshot-*/fixtures/**',
            rules: {
                'unicorn/prefer-module': 'off',
            },
        },
        {
            // TODO: Update tests.
            files: 'test-tap/**',
            rules: {
                'import/no-anonymous-default-export': 'off',
                'n/prefer-global/process': 'off',
                'unicorn/error-message': 'off',
            },
        },
    ],
};

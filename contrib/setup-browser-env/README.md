# `setup-browser-env`

[![postinstaller](https://postinstaller-badge.now.sh/postinstaller?style=flat-square)](https://github.com/postinstaller/postinstaller) [![build](https://img.shields.io/travis/AndreasPizsa/setup-browser-env.svg?style=flat-square)](https://travis-ci.org/AndreasPizsa/setup-browser-env) [![coverage](https://img.shields.io/coveralls/github/AndreasPizsa/setup-browser-env.svg?style=flat-square)](https://coveralls.io/github/AndreasPizsa/setup-browser-env) ![license](https://img.shields.io/github/license/AndreasPizsa/setup-browser-env.svg?style=flat-square) [![version](https://img.shields.io/npm/v/setup-browser-env.svg?style=flat-square)](https://www.npmjs.com/package/setup-browser-env) [![downloads](https://img.shields.io/npm/dm/setup-browser-env.svg?style=flat-square)](https://www.npmjs.com/package/setup-browser-env)

> Simplifies simulating a global browser environment using [browser-env][].

# Motivation

`setup-browser-env` simplifies simulating a global browser environment using [browser-env][] with zero configuration, keeping your project structure lean, clean & organized.

# Features

+   ✅ **Compatible.** Works with [ava][], [mocha][] and everything else.
+   ✅ **Zero Configuration** for ava. `npm add`, done.
+   ✅ **Configurable.** via `package.json` or `browser-env.{js, json, yaml}`
+   ✅ **Reliable.** 100% Code Coverage.
+   ✅ **Free.** MIT License.

# Usage

## Install

```sh
npm add -D setup-browser-env
```

### ava

##### Automatic configuration

If you’re using `ava` as a `devDependency`, installing `setup-browser-env` will configure ava automatically (using [postinstaller](http://github.com/postinstaller/postinstaller)).


##### Manual configuration

```json
// package.json
{
  "ava": {
    "require": [
      "setup-browser-env"
    ]
  }
}
```

### mocha

##### Manual configuration

```js
# mocha.opts
--require setup-browser-env
```

## Advanced Configuration

`setup-browser-env` runs out of the box without further configuration. You can still set options if needed in your `package.json` or a  `browser-env.{js,json,yaml}` config file.

To learn about all configuration options, please see [browser-env][] and [jsdom][].

#### package.json

```
{
  "browser-env": {
    "globals": ["window", "document"],
    "jsdom": {
      "userAgent": "My User Agent"
    }
  }
}
```

#### Shortcuts

Pass only the of name global properties without setting jsdom options:

```
{
  "browser-env": "window document"
}
```

```
{
  "browser-env": ["window", "document"]
}
```

Pass only jsdom options without setting the of name global properties:

```
{
  "browser-env": {
    "userAgent": "My User Agent"
  }
}
```

[ava]: https://github.com/avajs/ava
[mocha]: https://mochajs.org
[jsdom]: https://www.npmjs.com/package/jsdom
[browser-env]: https://www.npmjs.com/package/browser-env
[Andreas Pizsa]: https://twitter.com/AndreasPizsa
[license]: LICENSE.md

---

Copyright © 2018 [Andreas Pizsa][]. Licensed under the MIT [license][].

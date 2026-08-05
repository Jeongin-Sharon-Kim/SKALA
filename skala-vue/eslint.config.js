import pluginVue from 'eslint-plugin-vue'

export default [
  ...pluginVue.configs['flat/essential'],

  {
    files: ['**/*.{js,mjs,cjs,vue}'],

    rules: {
      eqeqeq: ['error', 'always'],
      'no-console': 'off',
    },
  },
]
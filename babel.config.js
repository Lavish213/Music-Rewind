module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          extensions: ['.ts', '.tsx', '.js', '.jsx'],
         alias: {
  '@ui': './frontend/src/ui',
  '@components': './frontend/src/ui/components',
  '@tokens': './frontend/src/ui/tokens',
  '@screens': './frontend/src/screens',
}
        },
      ],
    ],
  };
};
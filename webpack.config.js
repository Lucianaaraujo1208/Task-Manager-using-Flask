const path = require('path');

module.exports = {
  mode: 'development',  // ou 'production'
  entry: './src/index.js',  // ajuste o caminho conforme seu arquivo de entrada
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',  // se estiver usando Babel
        },
      },
      // adicione outras regras conforme necessário
    ],
  },
  devtool: 'source-map',  // para facilitar a depuração
};
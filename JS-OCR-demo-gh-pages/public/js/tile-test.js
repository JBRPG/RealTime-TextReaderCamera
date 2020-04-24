// import Tesseract from 'https://cdn.jsdelivr.net/gh/naptha/tesseract.js@v1.0.14/dist/tesseract.min.js';

Tesseract.recognize(
  'https://raw.githubusercontent.com/vanwars/RealTime-TextReaderCamera/master/JS-OCR-demo-gh-pages/public/img/letter_a.jpg',
  'eng',
  { logger: m => console.log(m) }
).then(response => {
    console.log(response);
    console.log(response.html);
});
const { createWorker } = require('tesseract.js')
const PSM = require('tesseract.js/src/constants/PSM.js')
const worker = createWorker()

async function getTextFromImage() {
  await worker.load()
  await worker.loadLanguage('eng')
  await worker.initialize('eng')
  await worker.setParameters({
    tessedit_pageseg_mode: PSM.AUTO,
  })

//   const { data: { text } } = await worker.recognize('./hello-world.png');
//   const { data: { text } } = await worker.recognize('./letter_a.jpg');
    const { data: { text } } = await worker.recognize('./tiles.png');


  await worker.terminate()

  return text
}

getTextFromImage()
  .then(console.log)

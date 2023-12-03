// Downlaod image from a webpage
async function downloadImage(image_src, name) {
    const image = await fetch(image_src)
    const image_blob = await image.blob()
    const image_url = URL.createObjectURL(image_blob)

    const link = document.createElement('a')
    link.href = image_url
    link.download = name
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
}

// The main grid of images in the CATPCHA
var CAPTCHA = document.getElementById('picture').getAttribute('src')
downloadImage(CAPTCHA, 'CAPTCHA')

// The first clue image
var clue1 = document.getElementById('c1').getAttribute('src')
downloadImage(clue1, 'clue1')

// The second clue image
var clue2 = document.getElementById('c2').getAttribute('src')
downloadImage(clue2, 'clue2')
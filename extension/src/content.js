const axios = require('axios');

async function getPrices(listings) {
    const response = await axios.post('https://lightnet.se/prices', listings)
    return response.data
}


function xPathOne(xpath, element) {
    return document.evaluate(xpath, element).iterateNext().textContent.trim()
}

function getAddress(listing) {
    var [address, floor] = xPathOne('.//div[1]/div[1]/h2/text()', listing).split(',')
    if (floor)
        floor = parseFloat(floor.replace(/\s+/g, ''))
    return {address, floor}
}

function getPrice(listing) {
    var price = xPathOne('.//div[2]/div[1]/div[1]/text()', listing)
    return parseFloat(price.replace(/\s+/g, ''));
}

function getSqm(listing) {
    var sqm = xPathOne('.//div[2]/div[1]/div[2]/text()', listing)
    return parseFloat(sqm.replace(/\s+/g, ''));
}

function getRooms(listing) {
    var rooms = xPathOne('.//div[2]/div[1]/div[3]/text()', listing)
    return parseFloat(rooms.replace(/\s+/g, ''));
}

function getRent(listing) {
    var rent = xPathOne('.//div[2]/div[2]/div[1]/text()', listing)
    return parseFloat(rent.replace(/\s+/g, ''));
}


async function predict() {
    var listings = document.evaluate('//*[@id="result"]/ul/li[*]/a/div[2]/div', document)

    var data = []
    while(listing = listings.iterateNext()) {
        data.push({
            ...getAddress(listing),
            price: getPrice(listing),
            sqm: getSqm(listing),
            rooms: getRooms(listing),
            rent: getRent(listing),
        })
    }


    const prices = await getPrices(data)
    var listingIndex = 1
    var priceIndex = 0
    while (priceIndex < prices.length) {
        var listing = document.evaluate(`//*[@id="result"]/ul/li[${listingIndex}]/a/div[2]/div/div[2]`, document).iterateNext()
        if (listing){
            const span = document.createElement('span')
            span.classList.add('predict')
            span.innerText = `${prices[priceIndex]} kr`;
            listing.append(span)
            priceIndex += 1
        }
        listingIndex += 1
    }

}
predict()
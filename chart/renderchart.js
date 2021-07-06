const puppeteer = require('puppeteer');

exports.renderChart = (req, res) => {
    estimate = req.body

    dictionary = {
        'United States of America (the)': 'US',
        'Argentina': 'AR',
        'Canada': 'CA',
        'Chile': 'CL',
        'China': 'CH',
        'Denmark': 'DK',
        'France': 'FR',
        'India': 'IN',
        'Ireland': 'IE',
        'Israel': 'IL',
        'Italy': 'IT',
        'Japan': 'JP',
        'Korea (the Republic of)': 'KR',
        'Mexico': 'MX',
        'Netherlands (the)': 'NL',
        'South Africa': 'ZA',
        'Switzerland': 'CH',
        'United Kingdom of Great Britain and Northern Ireland (the)': 'GB',
        'Bermuda': 'BM',
        'Cayman Islands (the)': 'KY',
        'Hong Kong': 'HK',
        'Indonesia': 'ID',
        'Macao': 'MC',
        'Malaysia': 'MY',
        'Pakistan': 'PK',
        'Philippines (the)': 'PH',
        'Singapore': 'SG',
        'Taiwan (Province of China)': 'TW',
        'Thailand': 'TH',
        'Australia': 'AU',
        'Austria': 'AT',
        'Belgium': 'BE',
        'Brazil': 'BR',
        'Colombia': 'CO',
        'Cyprus': 'CY',
        'Czechia': 'CZ',
        'Egypt': 'EG',
        'Finland': 'FI',
        'Germany': 'DE',
        'Greece': 'GL',
        'Hungary': 'HU',
        'Isle of Man': 'IM',
        'Kuwait': 'KW',
        'Luxembourg': 'LU',
        'New Zealand': 'NZ',
        'Norway': 'NO',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Qatar': 'QA',
        'Russian Federation (the)': 'RU',
        'Saudi Arabia': 'SA',
        'Spain': 'ES',
        'Sweden': 'SE',
        'Turkey': 'TR',
        'United Arab Emirates (the)': 'AE',
        'Papua New Guinea': 'PG',
        'Peru': 'PE',
        'Kenya': 'KE',
        'Morocco': 'MC',
        'Nigeria': 'NG',
        'Zimbabwe': 'ZW',
        'Puerto Rico': 'PR',
        'Uruguay': 'UQ',
        'Ukraine': 'UA',
        'Bangladesh': 'BD',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Oman': 'OM',
        'Romania': 'RO',
        'Sri Lanka': 'LK',
        'Viet Nam': 'VN',
        'Georgia': 'GE',
        'Iran (Islamic Republic of)': 'IR',
        'Croatia': 'HR',
        'Estonia': 'EE',
        'Lithuania': 'LT',
        'Afghanistan': 'AF',
        'Costa Rica': 'CR',
    }

    let exposure_list = [['Country', 'Exposure']]

    Object.keys(estimate).forEach(key => {
        if (dictionary[key]) exposure_list.push([dictionary[key], estimate[key]])
    })

    renderInBrowser(exposure_list).then(data => res.status(200).send(data))
};

async function renderInBrowser(list) {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()

    await page.addScriptTag({'url': 'https://www.gstatic.com/charts/loader.js'})
    await page.setContent('<div id="regions_div" style="width: 900px; height: 500px;"></div>')

    await page.exposeFunction("get_data", () => {return list});
    await page.evaluate(() => {
        google.charts.load('current', {
            'packages': ['geochart'],
            'mapsApiKey': 'AIzaSyAOzpYFJrO83tbQpSkuHD5gc3b9jPe9-YU'
        });

        google.charts.setOnLoadCallback(drawRegionsMap);

        async function drawRegionsMap() {
            const data = google.visualization.arrayToDataTable(await window.get_data());

            const options = {};
            const chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

            google.visualization.events.addListener(chart, 'ready', () => {
                window.imageURI = chart.getImageURI();
            });
            
            chart.draw(data, options);
        }
    })

    await page.waitForFunction('window.imageURI !== undefined')
    imageURI = await page.evaluate('window.imageURI')

    await browser.close()
    return imageURI
}

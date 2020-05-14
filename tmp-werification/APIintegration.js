function getForecast(){
	const token = '35f9b4a3ae7a274c1b12a8e3020ce69b180661ea';
	const requestData = {
	    model: 'um',
	    grid: 'P5',
	    coordinates: '120,120',
	    field: '03236_0000000',
	    level: '_',
	    date: '2019-04-10T12'
	}

	const requestPath = Object
	    .keys(requestData)
	    .filter(key => requestData[key].length > 0)
	    .map(key => `${key}/${requestData[key]}`)
	    .join('/')

	let path = `https://api.meteo.pl/api/v1/${requestPath}/forecast/`
	console.log(path)

	fetch(path, {
	    method: 'GET',
	    headers: {
		Authorization: `Authorization: Token ${token}`
	    }
	})
	    .then(response => response.json())
		.then(data => console.log(data))
		
	return data
};


function sh(cmd) {
	return new Promise(function (resolve, reject) {
	  exec(cmd, (err, stdout, stderr) => {
		if (err) {
		  reject(err);
		} else {
		  resolve({ stdout, stderr });
		}
	  });
	});
}

function getForecastExec(){
	cmd = `curl https://api.meteo.pl/api/v1/model/um/grid/P5/coordinates/120,120/field/03236_0000000/level/_/date/2019-04-10T12/forecast/ -X POST -H "Authorization: Token 35f9b4a3ae7a274c1b12a8e3020ce69b180661ea" > out.json`
	console.log("I am inside getForecastExec function");
	let { stdout } = sh('ls');
	for (let line of stdout.split('\n')) {
	  console.log(`ls: ${line}`);
	}
}
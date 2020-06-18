fs = require(fs);
var MongoClient = require("mongodb").MongoClient;
var url = "mongodb://127.0.0.1:27017/";

MongoClient.connect(url, function (err, db) {
  if (err) throw err;
  dbo = db.db("verificationservice");
});

function computeP(x, slope = 0.97, intercept = 0.084) {
  return 1 / (1 + Math.exp(slope * (x + intercept)));
}

function computeDescription(p, imgw) {
  descriptions = [
    [
      "TAK, owszem, przymrozka nie ma",
      "FAŁSZYWIE mnie poinformowałeś, że NIE MA przymrozka",
    ],
    [
      "FAŁSZYWIE mnie poinformaowałeś, że JEST przymrozek",
      "TAK, owszem, jest przymrozek",
    ],
  ];

  function verification(p, observ) {
    //default is "TAK, owszem, przymrozka nie ma"
    probabilityIndex = 0;
    verifIndex = 0;

    if (p > 0.1) {
      probabilityIndex = 1;
    }
    if (observ < 0) {
      verifIndex = 1;
    }
    return [verifIndex, probabilityIndex];
  }

  [verifIndex, probabilityIndex] = verification(p, imgw);
  console.log("verifindex is", verifIndex, "probIndex is", probabilityIndex);

  return descriptions[verifIndex][probabilityIndex];
}

//////////////////////////////////////////////////////////////////////////////////
////////historicals//////
//////////////////////////////////////////////////////////////////////////////////
let historicals = [];

//////////////////////////////////////////////////////////////////////////////////
///////forecast data/////
//////////////////////////////////////////////////////////////////////////////////
let forecast = [];

let diagonal = forecast.map((v) => ({
  value_imgw: v.value_imgw,
  value_um: v.value_imgw,
  category: "diagonal",
}));

let chart = new Taucharts.Chart({
  type: "scatterplot",
  data: forecast.concat(diagonal),
  x: "value_um",
  y: "value_imgw",
  color: "category",
  plugins: [
    Taucharts.api.plugins.get("tooltip")(),
    Taucharts.api.plugins.get("legend")(),
  ],
});
chart.renderTo("#taucharts_chart");

let effectiveness = historicals.concat(forecast).map((v) => ({
  value_um: v.value_um,
  p: computeP(v.value_um),
  description: computeDescription(computeP(v), v.value_imgw),
}));

let effectiveness_result = effectiveness.

let chart2 = new Taucharts.Chart({
  type: "scatterplot",
  data: effectiveness,
  x: "value_um",
  y: "p",
  color: "description",
  plugins: [
    Taucharts.api.plugins.get("tooltip")(),
    Taucharts.api.plugins.get("legend")(),
  ],
});
chart2.renderTo("#taucharts_chart2");

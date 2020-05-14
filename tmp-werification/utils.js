function computeP(x, slope = 0.3, intercept = 1.1) {
  return 1 / (1 + Math.exp(slope * (x + intercept)));
}

function linspace(a, b, n) {
  if (typeof n === "undefined") n = Math.max(Math.round(b - a) + 1, 1);
  if (n < 2) {
    return n === 1 ? [a] : [];
  }
  var i,
    ret = Array(n);
  n--;
  for (i = n; i >= 0; i--) {
    ret[i] = (i * b + (n - i) * a) / n;
    ret[i] = ret[i].toFixed(2);
  }
  return ret;
}

function time2str(num) {
  mCodes = [
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X",
    "XI",
    "XII",
  ];
  var qq = new Date(2016, 3, 5, 0);
  qq.setHours(qq.getHours() + num);
  var j = qq.getMinutes();
  if (j < 10) j = "0" + j;
  return (
    "" +
    qq.getDate() +
    " " +
    mCodes[qq.getMonth() - 1] +
    " " +
    qq.getHours() +
    ":" +
    j
  );
}

function RaphaelTable(
  data,
  width_cell = 30,
  height_cell = 20,
  stroke_array = 6,
  placediv = "table"
) {
  rows = data.length;
  w_column = width_cell + 2 * stroke_array;
  h_column = rows * height_cell + (rows + 1) * stroke_array;
  paper = Raphael(placediv, w_column, h_column);
  column = paper.rect(0, 0, w_column, h_column).attr("fill", "E0FFFF");
  for (let i = 0; i < rows; i++) {
    paper
      .rect(
        stroke_array,
        stroke_array + (height_cell + stroke_array) * i,
        width_cell,
        height_cell
      )
      .attr("fill", "48D1CC");
    paper.text(
      stroke_array + width_cell / 2,
      stroke_array + (height_cell + stroke_array) * i + height_cell / 2,
      data[i]
    );
  }
}

//implement legends and comments
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

statFault = [
  [-1, 0],
  [0, +1],
];

function mapColor(statFaultCell) {
  switch (statFaultCell) {
    case 0:
      return "888888";
      break;
    case -1:
      return "FFFF00";
      break;
    case +1:
      return "0000FF";
      break;
    default:
      return "FFFFFF";
  }
}

//mapping array values according to function pattern

function verification(p, observ) {
  //default is "TAK, owszem, przymrozka nie ma"
  probabilityIndex = 0;
  verifIndex = 0;
  if (p > 0.2) {
    probabilityIndex = 1;
  }
  if (observ < 0) {
    verifIndex = 1;
  }
  return [verifIndex, probabilityIndex];
}

function computePArray(arr, slope, intercept) {
  var newarr = [];
  arr.map((v, i) => {
    newarr.push(
      computeP(v, slope.children[0].value, intercept.children[0].value).toFixed(
        2
      )
    );
  });
  return newarr;
}

function computeDateArray(arr) {
  var newarr = [];
  arr.map((v, i) => {
    //console.warn(`${v}  ${i}`)
    newarr.push(time2str(v));
  });
  return newarr;
}

function computeVerifArray(probability, observ) {
  var newarr = [];
  //console.warn(`probarr${probability} observarr${observ} `)
  for (let i = 0; i < probability.length; i++) {
    //console.warn(`prob${probability[i]}, observ${observ[i]}`)
    let ix = verification(probability[i], observ[i]);
    let verif = ix[0];
    let prob = ix[1];
    //console.log(`indxes ${verif}  ${prob} ${ix}`)
    newarr.push(descriptions[verif][prob]);
  }

  return newarr;
}

//display and draw in raphael this arrays
function DrawRaphaelTables(obs, verifarr, p, simulation, date) {
  RaphaelTable(obs);
  RaphaelTable(verifarr, (width_cell = 450));
  columns = [p, simulation].reverse();
  columns.forEach((col, i) => {
    if (true) {
      RaphaelTable(col);
    }
  });
  RaphaelTable(date, (width_cell = 90));
}

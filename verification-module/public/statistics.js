function computeMockSigmoid(x, slope = 0.3, intercept = 1.1) {
  return 1 / (1 + Math.exp(slope * (x + intercept)));
}

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

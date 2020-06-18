function computeDescription(p, imgw) {
  descriptions = [
    ["NIE", "FAŁSZYWE NIE"],
    ["FAŁSZYWE TAK", "TAK"],
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

var demo_datas = [
  { p: 0.0, imgw: 1 },
  { p: 0.1, imgw: 2 },
  { p: 0.2, imgw: 3 },
  { p: 0.3, imgw: -1 },
  { p: 0.4, imgw: -2 },
  { p: 0.5, imgw: 1 },
];

demo_datas.map((r) => {
  console.log(`p: ${r.p}, imgw: ${r.imgw}, ${computeDescription(r.p, r.imgw)}`);
});

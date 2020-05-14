const express = require("express");
const bodyParser = require("body-parser");
const pino = require("express-pino-logger")();
const { exec } = require("child_process");
const mockdata = require("./mockdata.js");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(pino);

const data = {
  // "2019-09-09T12:00:00": JSON.stringify(mockdata.data),
};

app.get("/api/getResult", (req, res) => {
  const { from, to } = req.query;

  const filteredData = {};
  Object.keys(data).forEach((date) => {
    if ((!to || date <= to) && (!from || date >= from)) {
      filteredData[date] = data[date];
    }

    return;
  });

  res.setHeader("Content-Type", "application/json");
  res.send(JSON.stringify(filteredData));
});

const fetch = async (params) => {
  console.log("I am in fetch");
  // wyniesc do innego pliku
  // (moment(to) - moment(from))
  const dates = ["2016-03-05T00:00:00"]; // wyciagnac zakres dat z params i skonwertowac do tablicy dat oddzielonych godzinowo
  dates.forEach((date) => {
    // zrobić kolejkę, bo exec jest asynchroniczny i jest szansa na odpalenie tysiąca komend w konsoli
    let compiler = "python";
    let file = "umimgw_proceed/umimgw_proceed.py";
    //rc - abbrevation of rowcol
    let rc = [264, 280];
    let len = 6;
    let y = 2016;
    let m = 3;
    let d = 5;
    let h = 0;
    let command = `${compiler} ${file} ${len} ${rc[0]} ${rc[1]} ${y}-${m}-${d}T${h}`;
    console.log("path is:", command);
    exec(command, (err, stdout, stderr) => {
      if (err) {
        throw err;
      }
      console.log(`stdout from python is ${stdout}`);
      data[date] = JSON.parse(stdout);
    });
  });
};

app.get("/api/fetch", (req, res) => {
  const { from, to } = req.query;
  // dostoswac parametry
  fetch({
    from,
    to,
  })
    .then(() => {
      res.status(200);
      res.send();
    })
    .catch(() => {
      res.status(500);
      res.send();
    });
});

fetch();

app.listen(3001, () =>
  console.log("Express server is running on localhost:3001")
);

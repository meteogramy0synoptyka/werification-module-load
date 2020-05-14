import React from "react";
import moment from "moment";
import { computeMockSigmoid } from "../../utils/computeMockSigmoid";
import { useSelector } from "react-redux";

export function TableEntry({ date, value }) {
  console.log({ value });
  const { slope, intercept } = useSelector((state) => state.table);
  const momentDate = moment(date);
  const emptyArray = new Array(value.len_series).fill(true);

  return (
    <>
      {emptyArray.map((x, index) => {
        const currentDate = moment(+momentDate)
          .add(moment.duration(index, "hours"))
          .format("YYYY-MM-DDTHH:00:00");

        const p = computeMockSigmoid(value.um[index], slope, intercept).toFixed(
          5
        );

        return (
          <tr key={currentDate}>
            <td>{currentDate}</td>
            <td>{value.um[index]}</td>
            <td>{p}</td>
            <td>brak przymrozka</td>
            <td>{value.imgw[index]}</td>
          </tr>
        );
      })}
    </>
  );
}

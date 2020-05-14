import React from "react";
import { useSelector } from "react-redux";
import { TableEntry } from "./TableEntry";
import "./table.css";

export function Table() {
  const data = useSelector((state) => state.table.data);
  const dates = Object.keys(data);

  if (dates.length === 0) {
    return "Loading data...";
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <td>date</td>
          <td>um</td>
          <td>p</td>
          <td>description</td>
          <td>imgw</td>
        </tr>
      </thead>
      <tbody>
        {dates.map((date) => (
          <TableEntry key={date} date={date} value={data[date]} />
        ))}
      </tbody>
    </table>
  );
}

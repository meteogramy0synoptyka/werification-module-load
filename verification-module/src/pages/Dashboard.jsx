import React from "react";
import { Table } from "../components/table/Table";
import { TableConfig } from "../components//table/TableConfig";
import { useDispatch } from "react-redux";
import { addData } from "../store/reducers/table/actions";

export function Dashboard() {
  const dispatch = useDispatch();

  React.useEffect(() => {
    setTimeout(() => {
      fetch("http://localhost:3001/api/getResult")
        .then((data) => {
          return data.json();
        })
        .then((json) => {
          console.log({ json });
          dispatch(addData(json));
        });
    }, 30000);
  }, [dispatch]);

  return (
    <div>
      <div>
        <Table />
      </div>
      <div>
        <TableConfig />
      </div>
    </div>
  );
}

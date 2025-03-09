import { useState, useEffect } from "react";
import DefaultLayout from "@/layouts/default";
import { request } from "@/helpers/request";

export default function IndexPage() {
  function getCompoundList() {
    request.get("/compounds").then(({ data }) => {
      console.log(data);
    });
  }

  function getUser() {
    request.get("/current_user").then(({ data }) => {
      console.log(data);
    });
  }

  useEffect(() => {
    getCompoundList();
    getUser();
  }, []);

  return (
    <DefaultLayout>
      <div></div>
    </DefaultLayout>
  );
}

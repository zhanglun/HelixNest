import { useState, useEffect } from "react";
import DefaultLayout from "@/layouts/default";
import { request } from "@/helpers/request";
import { Button, Input } from "@heroui/react";

export default function IndexPage() {
  const [search, setSearch] = useState("");
  const [result, setResult] = useState<any>({});
  const [taskId, setTaskId] = useState("")
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

  function handleSearch() {
    request.get(`/compounds/query?cid=${search}`).then(({ data }) => {
      console.log(data);
      setResult(data);
    });
  }

  function startAnalysis(cid: number) {
    request
      .post("/compounds/start-analysis", {
        chemical: cid,
      })
      .then(({ data }) => {
        console.log(data);
        setTaskId(data.task_id)
      });
  }

  useEffect(() => {
    getCompoundList();
    getUser();
  }, []);

  return (
    <DefaultLayout>
      <div className="flex flex-row gap-3 items-center justify-center">
        <Input
          placeholder="add compounds, you can search with id or name"
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Button onPress={() => handleSearch()}>Search</Button>
      </div>
      <div>
        <div>
          {Object.keys(result).map((key: string) => {
            return (
              <p key={key}>
                {key} : {result[key] as any}
              </p>
            );
          })}
        </div>
        <div>
          <Button onPress={() => startAnalysis(result.pubchem_cid)}>
            Start analysis
          </Button>
        </div>
        <div>
          {taskId}
        </div>
      </div>
    </DefaultLayout>
  );
}

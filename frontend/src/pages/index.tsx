import { Button, Input } from "@heroui/react";
import { useState, useEffect } from "react";

import DefaultLayout from "@/layouts/default";
import { request } from "@/helpers/request";
import { CompoundCard } from "@/components/Compound/Card";

export default function IndexPage() {
  const [search, setSearch] = useState("");
  const [result, setResult] = useState<any>({});
  const [taskId, setTaskId] = useState("");
  const [list, setList] = useState([]);

  function getCompoundList() {
    request.get("/compounds").then(({ data }) => {
      setList(data.data?.compounds || []);
    });
  }

  function handleSearch() {
    request.get(`/compounds/query?cid=${search}`).then(({ data }) => {
      console.log(data);
      setResult(data);
    });
  }

  function handleInputEnter(e: React.KeyboardEvent<HTMLInputElement>) {
    const value = (e.target as HTMLInputElement).value;

    setSearch(value);

    if (e.key === "Enter") {
      handleSearch();
    }
  }

  function startAnalysis(cid: number) {
    request
      .post("/compounds/start-analysis", {
        chemical: cid,
      })
      .then(({ data }) => {
        const task_id = data.data.task_id;

        setTaskId(task_id);

        request.get(`/compounds/task-status/${task_id}`).then(({ data }) => {
          console.log(data);
        });
      });
  }

  useEffect(() => {
    getCompoundList();
  }, []);

  return (
    <DefaultLayout>
      <div className="flex flex-row gap-3 items-center justify-center">
        <Input
          placeholder="add compounds, you can search with id or name"
          type="text"
          value={search}
          onKeyUp={(e) => handleInputEnter(e)}
          onValueChange={(v) => setSearch(v)}
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
        <div>{taskId}</div>
      </div>
      <div className="grid grid-cols-1">
        {list.map((item: any) => {
          return <CompoundCard data={item} key={item.pubchem_cid} />;
        })}
      </div>
    </DefaultLayout>
  );
}

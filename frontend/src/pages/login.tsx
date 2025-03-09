import { Input } from "@heroui/input";
import { useEffect, useState } from "react";
import { addToast, Button } from "@heroui/react";
import { request } from "@/helpers/request";

export default function IndexPage() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin");

  function login() {
    request.post("/login", { username, password }).then((res) => {
      console.log(res);

      addToast("Login successful");
      // window.location.href = "/";
    });
  }

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-lg text-center justify-center">
        <Input
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          placeholder="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <Button onClick={login}>Login</Button>
      </div>
    </section>
  );
}

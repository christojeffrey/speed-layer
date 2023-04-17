import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("Well done!");
});

// get from postgres
// pg-promise
const pgp = require("pg-promise")();
const db = pgp("postgres://postgres:postgres@localhost:5432/mydb");

app.get("/users", async (req, res) => {
  const users = await db.any("SELECT * FROM social_media_stats");
  res.send(users);
});

app.listen(3000, () => {
  console.log("The application is listening on port 3000!");
});

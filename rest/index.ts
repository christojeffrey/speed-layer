import express from "express";

const app = express();

app.get("/", (req, res) => {
  res.send("Well done!");
});

// get from postgres
// pg-promise
const pgp = require("pg-promise")();
const db = pgp("postgres://postgres:postgres@localhost:5432/mydb");

app.get("/example", async (req, res) => {
  const users = await db.any("SELECT * FROM social_media_stats");
  res.send(users);
});

app.get("/results", async (req, res) => {
  // get start, end, social_media from query params
  const { start, end, social_media }: any = req.query;
  // return them
  // res.send({ start, end, social_media });
  // start and end is not optional, social_media is optional
  if (start === undefined || end === undefined) {
    res.status(400).send("Start and end date is required");
    return;
  }
  // format: YYYY-MM-DD HH:mm
  // check if format is correct using regex
  if (!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(end)) {
    res.status(400).send("Start and end date must be in format YYYY-MM-DD HH:mm");
    return;
  }
  if (social_media !== undefined) {
    if (!["facebook", "instagram", "twitter"].includes(social_media)) {
      res.status(400).send("Social media must be one of facebook, instagram or twitter");
      return;
    }
  }
  // print db valid columns
  // console.log(await db.any("SELECT column_name FROM information_schema.columns WHERE table_name = 'social_media_stats'"));
  try {
    let results;
    if (social_media !== undefined) {
      // get from db. format using TO_TIMESTAMP
      results = await db.any("SELECT * FROM social_media_stats WHERE created_at >= TO_TIMESTAMP($1, 'YYYY-MM-DD HH24:MI') AND created_at <= TO_TIMESTAMP($2, 'YYYY-MM-DD HH24:MI') AND social_media = $3", [start, end, social_media]);
    } else {
      results = await db.any("SELECT * FROM social_media_stats WHERE created_at >= TO_TIMESTAMP($1, 'YYYY-MM-DD HH24:MI') AND created_at <= TO_TIMESTAMP($2, 'YYYY-MM-DD HH24:MI')", [start, end]);
    }
    res.send(results);
  } catch (err) {
    console.log(err);
    res.status(500).send("Internal server error: " + err);
  }
});

app.listen(3000, () => {
  console.log("The application is listening on port 3000!");
});


const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');
const express = require('express');

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const queue = kue.createQueue();
const app = express();
const port = 1245;

let reservationEnabled = true;

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats;
}

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    let seats = await getCurrentAvailableSeats();
    seats--;
    if (seats === 0) {
      reservationEnabled = false;
    }
    if (seats >= 0) {
      await reserveSeat(seats);
      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});

queue.on('job complete', (id, result) => {
  console.log(`Seat reservation job ${id} completed`);
});

queue.on('job failed', (id, err) => {
  console.log(`Seat reservation job ${id} failed: ${err.message}`);
});


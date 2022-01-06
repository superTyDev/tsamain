// Load required modules
var http = require("http"); // http server core module
var express = require("express"); // web framework external module
var socketIo = require("socket.io"); // web socket external module

// Set process name
process.title = "tsaevent";

// Get port or default to 8080
var port = process.env.PORT || 8080;

// Setup and configure Express http server. Expect a subfolder called "static" to be the web root.
var app = express();
app.use(express.static("public"));

// Start Express http server
var webServer = http.createServer(app);
// var socketServer = socketIo.listen(webServer, { "log level": 1 });
const io = socketIo(webServer, { "log level": 1 });

const rooms = {};

io.on("connection", (socket) => {
	console.log("user connected", socket.id);

	let curRoom = null;

	socket.on("joinRoom", (data) => {
		const { room } = data;

		if (!rooms[room]) {
			rooms[room] = {
				name: room,
				occupants: {},
			};
		}

		const joinedTime = Date.now();
		rooms[room].occupants[socket.id] = joinedTime;
		curRoom = room;

		console.log(`${socket.id} joined room ${room}`);
		socket.join(room);

		socket.emit("connectSuccess", { joinedTime });
		const occupants = rooms[room].occupants;
		io.in(curRoom).emit("occupantsChanged", { occupants });
	});

	socket.on("send", (data) => {
		io.to(data.to).emit("send", data);
	});

	socket.on("broadcast", (data) => {
		socket.to(curRoom).broadcast.emit("broadcast", data);
	});

	socket.on("disconnect", () => {
		console.log("disconnected: ", socket.id, curRoom);
		if (rooms[curRoom]) {
			console.log("user disconnected", socket.id);

			delete rooms[curRoom].occupants[socket.id];
			const occupants = rooms[curRoom].occupants;
			socket.to(curRoom).broadcast.emit("occupantsChanged", { occupants });

			if (occupants == {}) {
				console.log("everybody left room");
				delete rooms[curRoom];
			}
		}
	});
});

webServer.listen(port, () => {
	console.log("listening on http://localhost:" + port);
});

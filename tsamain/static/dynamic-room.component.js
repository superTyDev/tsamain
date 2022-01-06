/**
 * Setup the Networked-Aframe scene component based on query parameters
 */
AFRAME.registerComponent("dynamic-room", {
	init: function () {
		var el = this.el;
		var params = this.getUrlParams();

		if (!params.room) {
			window.alert("Please add a room name in the URL, eg. ?room=myroom");
		}

		// Setup networked-scene
		var networkedComp = {
			room: params.room,
			debug: true,
			connectOnLoad: false,
		};
		console.info("Init networked-aframe with settings:", networkedComp);
		el.setAttribute("networked-scene", networkedComp);

		var scene = document.querySelector("a-scene");

		if (scene.hasLoaded) {
			this.onSceneLoad(params);
		} else {
			scene.addEventListener("loaded", (params) => {
				this.onSceneLoad(params);
			});
		}
	},

	getUrlParams: function () {
		var match;
		var pl = /\+/g; // Regex for replacing addition symbol with a space
		var search = /([^&=]+)=?([^&]*)/g;
		var decode = function (s) {
			return decodeURIComponent(s.replace(pl, " "));
		};
		var query = window.location.search.substring(1);
		var urlParams = {};

		match = search.exec(query);
		while (match) {
			urlParams[decode(match[1])] = decode(match[2]);
			match = search.exec(query);
		}
		return urlParams;
	},

	onSceneLoad: function (params) {
		var username;
		if (params.username) {
			username = params.username;
		} else {
			username = prompt("Choose a username");
		}

		var myNametag = document.getElementById("player").querySelector(".nametag");
		myNametag.setAttribute("text", "value", username);
		switchAvatar();

		document.querySelector("a-scene").components["networked-scene"].connect();
	},
});

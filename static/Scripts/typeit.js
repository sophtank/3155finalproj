if (document.getElementById("user-name")) {
  new TypeIt("#user-name", {
    speed: 100,
  })
    .pause(700)
    .delete(1)
    .pause(400)
    .type("!")
    .pause(300)
    .go();
} else if (document.getElementById("drive")) {
  new TypeIt("#drive", {
    speed: 100,
  })
    .type("Recnt")
    .pause(400)
    .move(-2)
    .type("e")
    .pause(400)
    .move(3)
    .type(" Drive")
    .pause(800)
    .type("s")
    .go();
} else if (document.getElementById("create-drive")) {
  new TypeIt("#create-drive", {
    speed: 125,
  })
    .type("Create Drive")
    .pause(800)
    .move(-5)
    .pause(200)
    .type("a")
    .pause(400)
    .type(" ")
    .pause(400)
    .move(5)
    .go();
} else if (document.getElementById("edit-drive")) {
  new TypeIt("#edit-drive", {
    speed: 125,
  })
    .type("edit a drive")
    .pause(800)
    .move(-4)
    .delete(1)
    .type("D")
    .pause(200)
    .move(-7)
    .pause(200)
    .delete(1)
    .type("E")
    .pause(400)
    .move(11)
    .go();
}

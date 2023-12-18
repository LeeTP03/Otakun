data = [
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/1-7bab07fbf9a2622325ade433f7889f61953f6f11f821a08f4ed1f59ff1efe11e.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/2-06df30e2098fe7224b340f25848fca7efb0a9cd06d23f22ebcecc7857aa40d7a.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/3-42c6019d0fe30cfdf361fe5ca3362a78f998952796521b048e7dfc60eaf73d2a.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/4-417967fdf729ea8903a97cd7fd65ad94947c66086e29d7ac19504796cf172ad4.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/5-98934ff27dadbebf3c855ff0fd2d68a2b37f837db855a8329709402fcadd79ad.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/6-6364dd9ccce06891ecfdc4cdc09072cfa1072e85fe1a2f29998d3dbb1e3923d7.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/7-b68e8191b8716d9264eb4d1f74ceaff4dc6ca0b5b41351017eca0629a83f5656.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/8-676b398a16769fe5774fcdd219012864c885eae11727f0cbd657aa9ddd4f032d.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/9-56cc77ef4f1471206a07975d908a84e034f92d849a28f3021c1b871887489308.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/10-49177f02bffe6326b72c2c9c92cb2f2d17082ba0a08c055033b63a4ada1b13cb.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/11-fec01761ecf498dc5020c5ab651c86ae5986dbc8ca38e0fb1aa55086c2b8adbb.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/12-f36144d5d88f530baa9b57edbadb6980df71cb49b3daf8329eb824e5162ce83c.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/13-1a875b88c11486d1ffad5d462267b06d79ea7ce7048538151bbc5bba371be0dd.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/14-5d13c098ced25c2e8126690d8ba5a514b20960ce12436d12b16220ea78107dbe.jpg",
    "https://uploads.mangadex.org/data-saver/85423d90d3bf8ccb3a5d0124b67e618b/15-0a0e3466b7a755d4af7d97e35b8a77872ed1979f15713a3a16ad357bfe3bfd4f.jpg",
]

data = [
    i.replace(
        "https://uploads.mangadex.org/data-saver/", "https://fxmangadex.org/data-saver/"
    )
    for i in data
]


print(data)

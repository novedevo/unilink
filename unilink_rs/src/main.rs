
use rspotify::{
    self, client::Spotify, model::search::SearchResult, oauth2::SpotifyClientCredentials,
};

const CLIENT_ID: &str = "PLACEHOLDER";
const CLIENT_SECRET: &str = "PLACEHOLDER";

enum Item {
    Track(Track),
    Album(Album),
    Artist(Artist),
}

enum ItemDiscriminant {
    Track,
    Album,
    Artist,
}

struct SpotifyUrl {
    discriminant: ItemDiscriminant,
    url: String,
}

struct Track {
    name: String,
    album: String,
    artist: String,
}

struct Album {
    name: String,
    artist: String,
}

struct Artist {
    name: String,
}

#[tokio::main]
async fn main() {
    let client_credentials_manager = SpotifyClientCredentials::default()
        .client_id(CLIENT_ID)
        .client_secret(CLIENT_SECRET)
        .build();
    let sp = Spotify::default()
        .client_credentials_manager(client_credentials_manager)
        .build();

    let url = "https://open.spotify.com/track/337H7R2AWIlI9s7M4ugelQ?si=92b3988a139746c7";
    let disc = ItemDiscriminant::Track;

    let url = SpotifyUrl {
        discriminant: disc,
        url: url.to_string(),
    };

    let item = parse_spotify_url(&url, &sp).await.unwrap();

    let new_url = get_spotify_url(&item, &sp).await.unwrap();

    assert_eq!(new_url, url.url);
}

async fn parse_spotify_url(url: &SpotifyUrl, sp: &Spotify) -> Option<Item> {
    let uri = url.url.split('?').next()?.split('/').last()?;
    match url.discriminant {
        ItemDiscriminant::Artist => Some(Item::Artist(Artist {
            name: sp.artist(uri).await.ok()?.name,
        })),
        ItemDiscriminant::Album => {
            let album = sp.album(uri).await.ok()?;
            Some(Item::Album(Album {
                name: album.name,
                artist: album.artists.first().unwrap().name.clone(),
            }))
        }
        ItemDiscriminant::Track => {
            let track = sp.track(uri).await.ok()?;
            Some(Item::Track(Track {
                name: track.name,
                album: track.album.name.clone(),
                artist: track.artists.first().unwrap().name.clone(),
            }))
        }
    }
}

async fn get_spotify_url(item: &Item, sp: &Spotify) -> Option<String> {
    match item {
        Item::Artist(artist) => {
            if let SearchResult::Artists(artists) = sp
                .search(
                    &artist.name,
                    rspotify::senum::SearchType::Artist,
                    1,
                    0,
                    None,
                    None,
                )
                .await
                .ok()?
            {
                Some(artists.items.first()?.href.clone())
            } else {
                unreachable!()
            }
        }
        Item::Album(album) => {
            if let SearchResult::Albums(albums) = sp
                .search(
                    &format!("{} {}", album.name, album.artist),
                    rspotify::senum::SearchType::Album,
                    1,
                    0,
                    None,
                    None,
                )
                .await
                .ok()?
            {
                Some(albums.items.first()?.href.as_ref()?.clone())
            } else {
                unreachable!()
            }
        }
        Item::Track(track) => {
            if let SearchResult::Tracks(tracks) = sp
                .search(
                    &format!("{} {} {}", track.name, track.album, track.artist),
                    rspotify::senum::SearchType::Track,
                    1,
                    0,
                    None,
                    None,
                )
                .await
                .ok()?
            {
                Some(tracks.items.first()?.href.as_ref()?.clone())
            } else {
                unreachable!()
            }
        }
    }
}

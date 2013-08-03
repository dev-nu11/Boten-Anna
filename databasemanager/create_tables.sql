create table urls ( uid integer PRIMARY KEY,
                    url text,
                    page_title text,
                    message text,
                    user text,
                    timestamp datetime default current_timestamp
                   );

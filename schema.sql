drop table if exists notifications;

create table notifications (
    "id" integer primary key,
    "timestamp" datetime default CURRENT_TIMESTAMP not null,
    "title" text not null,
    "body" text not null
);

create index "notifications_title_idx" on notifications (title asc);
create index "notifications_body_idx" on notifications (body asc);

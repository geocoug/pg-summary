drop table if exists public.genres cascade;
create table public.genres (
    genre varchar(100) primary key,
    description varchar not null
);

drop table if exists public.books cascade;
create table public.books (
    book_id varchar(100) primary key,
    book_title varchar(200) not null,
    genre varchar(100) not null,
    notes text,
    foreign key (genre) references public.genres(genre)
);

drop table if exists public.authors cascade;
create table public.authors (
    author_id varchar(100) primary key,
    first_name varchar(100) not null,
    last_name varchar(100) not null,
    constraint chk_authors check (first_name <> last_name),
    constraint chk_authors_first_name check (first_name ~ '^[a-zA-Z]+$'),
    constraint chk_authors_last_name check (last_name ~ '^[a-zA-Z]+$')
);

drop table if exists public.book_authors cascade;
create table public.book_authors (
    book_id varchar(100) not null,
    author_id varchar(100) not null,
    foreign key (author_id) references public.authors(author_id),
    foreign key (book_id) references public.books(book_id),
    constraint pk_book_authors primary key (book_id, author_id)
);

-- Insert data into staging tables.
insert into public.genres (genre, description) values
    ('Fiction', 'Literary works that are imaginary, not based on real events or people'),
    ('Non-Fiction', 'Literary works based on real events, people, and facts');

insert into public.authors (author_id, first_name, last_name) values
    ('JDoe', 'John', 'Doe'),
    ('JSmith', 'Jane', 'Smith'),
    ('JTrent', 'Joe', 'Trent');

insert into public.books (book_id, book_title, genre, notes) values
    ('B001', 'The Great Novel', 'Fiction', 'An epic tale of love and loss'),
    ('B002', 'Not Another Great Novel', 'Non-Fiction', 'A comprehensive guide to writing a great novel');

insert into public.book_authors (book_id, author_id) values
    ('B001', 'JDoe'),
    ('B001', 'JTrent'),
    ('B002', 'JSmith');

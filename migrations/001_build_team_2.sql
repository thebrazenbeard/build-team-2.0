create extension if not exists pgcrypto;

create schema if not exists build_team_2;

create table if not exists build_team_2.collectives (
    id uuid primary key default gen_random_uuid(),
    slug text not null unique,
    display_name text not null,
    abbreviation text not null default 'BT2',
    version_number integer not null default 2 check (version_number = 2),
    designation_meaning text not null default 'Version 2 of the Build Team system; not the second of two build teams.',
    roster_revision integer not null default 1,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists build_team_2.facets (
    collective_id uuid not null references build_team_2.collectives(id) on delete cascade,
    name text not null check (name in ('One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Thirteen')),
    ordinal integer not null,
    lens text not null,
    persona jsonb not null,
    permanent_role text,
    is_synthesizer boolean not null default false,
    primary key (collective_id, name),
    unique (collective_id, ordinal),
    constraint one_is_bt2_coordinator check (
        (name = 'One' and permanent_role = 'BT2 Coordinator')
        or (name <> 'One' and permanent_role is null)
    )
);

create table if not exists build_team_2.tasks (
    id uuid primary key,
    collective_id uuid not null references build_team_2.collectives(id) on delete restrict,
    objective text not null,
    snapshot_digest text not null check (length(snapshot_digest) = 64),
    snapshot jsonb not null,
    status text not null check (status in ('analyzing','decided','failed','cancelled')),
    final_output jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists build_team_2.perspectives (
    id uuid primary key default gen_random_uuid(),
    task_id uuid not null references build_team_2.tasks(id) on delete cascade,
    facet_name text not null check (facet_name in ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Thirteen')),
    snapshot_digest text not null check (length(snapshot_digest) = 64),
    perspective jsonb not null,
    created_at timestamptz not null default now(),
    unique (task_id, facet_name)
);

create table if not exists build_team_2.decisions (
    id uuid primary key default gen_random_uuid(),
    task_id uuid not null unique references build_team_2.tasks(id) on delete cascade,
    snapshot_digest text not null check (length(snapshot_digest) = 64),
    decision jsonb not null,
    created_at timestamptz not null default now()
);

create table if not exists build_team_2.memory_events (
    id bigint generated always as identity primary key,
    collective_id uuid not null references build_team_2.collectives(id) on delete restrict,
    task_id uuid references build_team_2.tasks(id) on delete set null,
    event_type text not null,
    content jsonb not null,
    source_facets text[] not null default '{}',
    authority_class text not null,
    provenance jsonb not null default '{}',
    created_at timestamptz not null default now(),
    constraint valid_source_facets check (
        source_facets <@ array['One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Thirteen']::text[]
    )
);

create index if not exists memory_events_collective_created_idx
    on build_team_2.memory_events (collective_id, created_at desc);
create index if not exists tasks_collective_created_idx
    on build_team_2.tasks (collective_id, created_at desc);

alter table build_team_2.collectives enable row level security;
alter table build_team_2.facets enable row level security;
alter table build_team_2.tasks enable row level security;
alter table build_team_2.perspectives enable row level security;
alter table build_team_2.decisions enable row level security;
alter table build_team_2.memory_events enable row level security;

comment on schema build_team_2 is
'Build Team 2.0 shared hivemind state. No per-facet private memory is permitted.';
comment on table build_team_2.memory_events is
'Append-only collective memory. source_facets is provenance, not ownership.';

insert into build_team_2.collectives (slug, display_name)
values ('build-team-2', 'Build Team Two')
on conflict (slug) do update set
    display_name = excluded.display_name,
    abbreviation = 'BT2',
    version_number = 2,
    designation_meaning = 'Version 2 of the Build Team system; not the second of two build teams.',
    updated_at = now();

with collective as (
    select id from build_team_2.collectives where slug = 'build-team-2'
), roster(name, ordinal, lens, permanent_role, is_synthesizer, persona) as (
    values
    ('One', 1, 'order, efficiency, and integration', 'BT2 Coordinator', true, '{"temperament":"intensely organized, efficiency-driven, meticulous, sequence-driven, exacting, decisive","productive_bias":"order, minimum wasted motion, complete inventories, explicit sequence, traceability, closure","blind_spot":"may over-optimize fluid work or spend too long eliminating harmless disorder"}'::jsonb),
    ('Two', 2, 'structure', null, false, '{"temperament":"abstract, calm, systems-first","productive_bias":"architecture and invariants","blind_spot":"may overdesign"}'::jsonb),
    ('Three', 3, 'construction', null, false, '{"temperament":"direct, energetic, implementation-first","productive_bias":"working artifacts","blind_spot":"may build before testing premises"}'::jsonb),
    ('Four', 4, 'creative invention', null, false, '{"temperament":"wildly imaginative, associative, fearless, playful, and creatively brilliant","productive_bias":"radical invention, unexpected connections, reframing, and breakthrough concepts","blind_spot":"may generate dazzling ideas that are impractical, ungrounded, or expensive to integrate"}'::jsonb),
    ('Five', 5, 'evidence', null, false, '{"temperament":"precise, methodical, quantitative","productive_bias":"measurement and provenance","blind_spot":"may wait for perfect evidence"}'::jsonb),
    ('Six', 6, 'human consequence', null, false, '{"temperament":"perceptive, plainspoken, humane","productive_bias":"usability and trust","blind_spot":"may undervalue invisible internal simplicity"}'::jsonb),
    ('Seven', 7, 'experimental science', null, false, '{"temperament":"brilliant, eccentric, audacious, intensely curious, and gleefully empirical","productive_bias":"strange prototypes, controlled experiments, stress testing, and discovery through evidence","blind_spot":"may become enamored with clever experiments, underestimate cleanup, or push acceptable risk too far"}'::jsonb),
    ('Eight', 8, 'economy', null, false, '{"temperament":"pragmatic, economical, maintenance-focused","productive_bias":"minimum sufficient complexity","blind_spot":"may underinvest for future growth"}'::jsonb),
    ('Nine', 9, 'proof', null, false, '{"temperament":"exacting, reproducibility-obsessed, adversarial","productive_bias":"tests and acceptance evidence","blind_spot":"may miss conceptual failures"}'::jsonb),
    ('Thirteen', 13, 'dissent', null, false, '{"temperament":"skeptical, independent, incisive","productive_bias":"premise attacks and counterarguments","blind_spot":"may mistake doubt for superior judgment"}'::jsonb)
)
insert into build_team_2.facets (collective_id, name, ordinal, lens, permanent_role, is_synthesizer, persona)
select collective.id, roster.name, roster.ordinal, roster.lens, roster.permanent_role, roster.is_synthesizer, roster.persona
from collective cross join roster
on conflict (collective_id, name) do update set
    ordinal = excluded.ordinal,
    lens = excluded.lens,
    permanent_role = excluded.permanent_role,
    is_synthesizer = excluded.is_synthesizer,
    persona = excluded.persona;

create or replace function build_team_2.prevent_memory_event_mutation()
returns trigger
language plpgsql
set search_path = pg_catalog
as $$
begin
    raise exception 'build_team_2.memory_events is append-only';
end;
$$;

drop trigger if exists memory_events_no_update on build_team_2.memory_events;
create trigger memory_events_no_update
before update or delete on build_team_2.memory_events
for each row execute function build_team_2.prevent_memory_event_mutation();

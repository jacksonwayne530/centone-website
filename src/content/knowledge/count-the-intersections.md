---
title: Count the Intersections
description: Street connectivity may be the most important number in neighborhood design, and almost nobody regulates it.
cover: ./covers/count-the-intersections.svg
date: 2026-09-21
order: 0
---

When a neighborhood is proposed, the arguments are almost always about the buildings: how tall, how dense, how many parking spaces, what they'll look like. Those things matter. But one of the strongest predictors of whether people will walk, how much they'll drive, and how safe they'll be getting around is something much plainer, and it gets decided long before anyone argues about a building.

It's the number of intersections per square mile.

## What intersection density measures

Intersection density is exactly what it sounds like: how many places streets meet within a given area. It's a stand-in for the shape of the street network. A traditional grid of short blocks produces lots of intersections. A postwar subdivision of looping collector roads, cul-de-sacs, and a single entrance onto an arterial produces very few, even if the houses are just as close together.

The difference shows up in the most ordinary trip. In a connected grid, the corner store two blocks away really is two blocks away. In a disconnected pod, the store behind your back fence might be a mile's drive: out the cul-de-sac, down the collector, onto the arterial, and back in. The houses are the same distance apart. The network isn't.

<figure class="graphic diagram">
  <p class="g-title">Same distance, different network</p>
  <svg viewBox="0 0 560 300" role="img" aria-label="Two street maps. Left: a connected grid with 25 intersections, where the walk from home to the store is two blocks. Right: a cul-de-sac subdivision with 5 intersections, where the store is just past the back fence but the trip goes out the cul-de-sac, down the collector road, along the arterial, and back in.">
    <g class="road" stroke-width="9"><line x1="20" y1="20" x2="20" y2="240"/><line x1="20" y1="20" x2="240" y2="20"/><line x1="75" y1="20" x2="75" y2="240"/><line x1="20" y1="75" x2="240" y2="75"/><line x1="130" y1="20" x2="130" y2="240"/><line x1="20" y1="130" x2="240" y2="130"/><line x1="185" y1="20" x2="185" y2="240"/><line x1="20" y1="185" x2="240" y2="185"/><line x1="240" y1="20" x2="240" y2="240"/><line x1="20" y1="240" x2="240" y2="240"/></g>
    <circle class="node" cx="20" cy="20" r="4"/><circle class="node" cx="20" cy="75" r="4"/><circle class="node" cx="20" cy="130" r="4"/><circle class="node" cx="20" cy="185" r="4"/><circle class="node" cx="20" cy="240" r="4"/><circle class="node" cx="75" cy="20" r="4"/><circle class="node" cx="75" cy="75" r="4"/><circle class="node" cx="75" cy="130" r="4"/><circle class="node" cx="75" cy="185" r="4"/><circle class="node" cx="75" cy="240" r="4"/><circle class="node" cx="130" cy="20" r="4"/><circle class="node" cx="130" cy="75" r="4"/><circle class="node" cx="130" cy="130" r="4"/><circle class="node" cx="130" cy="185" r="4"/><circle class="node" cx="130" cy="240" r="4"/><circle class="node" cx="185" cy="20" r="4"/><circle class="node" cx="185" cy="75" r="4"/><circle class="node" cx="185" cy="130" r="4"/><circle class="node" cx="185" cy="185" r="4"/><circle class="node" cx="185" cy="240" r="4"/><circle class="node" cx="240" cy="20" r="4"/><circle class="node" cx="240" cy="75" r="4"/><circle class="node" cx="240" cy="130" r="4"/><circle class="node" cx="240" cy="185" r="4"/><circle class="node" cx="240" cy="240" r="4"/>
    <path class="route" d="M102 150V130H157V112"/>
    <path class="home" d="M94 163V155L102 148L110 155V163Z"/>
    <rect class="store" x="145" y="88" width="24" height="18" rx="2"/>
    <text x="0" y="272" class="label">CONNECTED GRID</text>
    <text x="0" y="290" class="small">25 intersections · a 2-block walk</text>
    <g class="road"><path d="M300 240H560" stroke-width="14"/><path d="M330 240V50H520M330 110H400M330 170H400M450 50V120M480 240V192" stroke-width="9"/><circle cx="400" cy="110" r="6" stroke-width="12"/><circle cx="400" cy="170" r="6" stroke-width="12"/><circle cx="450" cy="120" r="6" stroke-width="12"/></g>
    <circle class="node" cx="330" cy="110" r="4"/><circle class="node" cx="330" cy="170" r="4"/><circle class="node" cx="330" cy="240" r="4"/><circle class="node" cx="450" cy="50" r="4"/><circle class="node" cx="480" cy="240" r="4"/>
    <line class="fence" x1="448" y1="142" x2="448" y2="206"/>
    <path class="route" d="M420 170H330V240H480V196"/>
    <path class="home" d="M416 178V170L424 163L432 170V178Z"/>
    <rect class="store" x="468" y="168" width="24" height="18" rx="2"/>
    <text x="300" y="272" class="label">CUL-DE-SAC POD</text>
    <text x="300" y="290" class="small">5 intersections · a drive all the way around</text>
  </svg>
  <figcaption>The home and the store are about the same distance apart in both. In the pod, the back fence (red) blocks the direct route, so the trip goes out the cul-de-sac, down the collector, along the arterial, and back in. Dots mark intersections.</figcaption>
</figure>

## Why it matters

### People walk where the streets connect

In 2010, Reid Ewing and Robert Cervero pooled the findings of dozens of studies on travel and the built environment into what is still the most-cited meta-analysis in the field. Walking, they found, was most strongly tied to land-use mix, intersection density, and the number of destinations within walking distance. The single largest effect they found for any variable, on any kind of travel, was intersection density's effect on walking.[^ewing2010]

Connected networks make walking trips shorter and give people more route choices, so more trips fall within walking range. A density bonus can't do that. You can double the number of homes in a cul-de-sac development and still leave everyone a mile's drive from the corner store.

### People drive less

The same research found that intersection density and the share of four-way intersections each have a measurable effect on how much people drive. In Ewing and Cervero's weighted averages, each carried an elasticity of about −0.12 for vehicle miles traveled. That's three times the effect of household density, which came in at −0.04.[^ewing2017] Density gets most of the attention in debates about driving. Street design quietly does more.

<figure class="graphic">
  <p class="g-title">How much less people drive, per 10% increase</p>
  <ul class="bars">
    <li><span>Intersection density</span><span class="bar-track"><span class="bar accent" style="--v: 100">−1.2%</span></span></li>
    <li><span>Share of 4-way intersections</span><span class="bar-track"><span class="bar accent" style="--v: 100">−1.2%</span></span></li>
    <li><span>Household density</span><span class="bar-track"><span class="bar" style="--v: 33">−0.4%</span></span></li>
  </ul>
  <figcaption>Change in vehicle miles traveled for a 10% increase in each factor, from weighted-average elasticities of −0.12, −0.12, and −0.04. Source: Ewing &amp; Cervero (2010; restated 2017).</figcaption>
</figure>

### Streets get safer

Wesley Marshall and Norman Garrick studied 11 years of crash data, more than 230,000 crashes, across 24 California cities. Denser street networks with more intersections per square mile were associated with fewer crashes at every level of severity: total, severe-injury, and fatal. Moving from average to the highest intersection density was associated with about 30 percent fewer total crashes.[^marshall2011] In their earlier comparison of the same cities, the safer cities had far more intersections per square mile and about a third as many traffic deaths per capita as the most dangerous ones.[^marshall2010]

<figure class="graphic">
  <p class="g-title">Connected streets and crashes in 24 California cities</p>
  <ul class="stats">
    <li><strong>230,000+</strong>Crashes studied over 11 years</li>
    <li><strong>~30%</strong>Fewer total crashes going from average to the highest intersection density</li>
    <li><strong>~⅓</strong>The traffic deaths per capita in the safest cities, compared with the most dangerous</li>
  </ul>
  <figcaption>Sources: Marshall &amp; Garrick (2010, 2011).</figcaption>
</figure>

That may seem backwards, since intersections are where cars collide. But connected networks spread traffic across many small streets, keeping speeds low. Disconnected networks funnel everything onto a few wide, fast arterials. Marshall and Garrick found that more travel lanes on major streets went with *more* crashes. That's a big part of why this site also argues that [city streets rarely need more than three lanes](/knowledge/three-lanes-25-mph/).

### People are healthier

Marshall, Garrick, and Daniel Piatkowski then compared the same 24 cities with state health survey data. Higher intersection density was significantly associated with lower obesity rates at the neighborhood level. At the city level, it was associated with lower rates of obesity, diabetes, high blood pressure, and heart disease.[^marshall2014] The pattern held with income and other factors taken into account. Streets that make walking the easy choice appear to show up in people's bodies.

## Why almost nobody regulates it

If connectivity matters this much, why isn't it at the center of land-use policy? There are a few reasons.

**Zoning doesn't cover it.** Zoning codes regulate what can be built on a lot: its use, height, density, and setbacks. The street network is set elsewhere, in subdivision regulations and engineering standards, usually once, when farmland is first carved up. After that it's close to permanent.

**Street networks last.** Christopher Barrington-Leigh and Adam Millard-Ball measured the connectivity of every street built in the United States from 1920 to 2012. Street-network sprawl rose steadily for most of the century and peaked around 1994. New streets have become somewhat more connected since, but places built with disconnected networks tend to stay that way, even as they grow.[^barrington2015] Buildings get replaced every few generations. Street layouts can last for centuries.

**The rules were written against the grid.** In the late 1930s, the Federal Housing Administration's guidance for developers seeking federally insured mortgages presented curving streets and cul-de-sacs as good design and the traditional grid as bad.[^fha1938] What began as advice became the national default. Jane Jacobs was already pushing back in 1961, with a whole chapter of *The Death and Life of Great American Cities* titled "The Need for Small Blocks."[^jacobs1961]

**It's easy to lose politically.** In 2009, Virginia began requiring new subdivision streets to meet a minimum "connectivity index" before the state would take over their maintenance, a first-of-its-kind rule.[^ggwash] Home builders fought it from the start.[^bizsense] After the legislature ordered a review, the state dropped the index entirely, effective January 2012. What remained was a much weaker rule requiring extra external connections only for large subdivisions.[^vdot2011]

<figure class="graphic">
  <p class="g-title">How the grid lost, and keeps losing</p>
  <ol class="timeline">
    <li class="key"><span class="year">1938</span><span>FHA's <em>Planning Profitable Neighborhoods</em> promotes curving streets and cul-de-sacs over the grid for federally insured developments.</span></li>
    <li><span class="year">1961</span><span>Jane Jacobs argues for "The Need for Small Blocks" in <em>The Death and Life of Great American Cities</em>.</span></li>
    <li class="key"><span class="year">1994</span><span>Street-network sprawl in new U.S. development peaks.</span></li>
    <li><span class="year">2009</span><span>Virginia requires new subdivision streets to meet a connectivity index.</span></li>
    <li class="key"><span class="year">2012</span><span>After pushback from home builders, Virginia drops the index.</span></li>
  </ol>
</figure>

## What to do about it

- **Measure it.** Intersection density is easy to calculate from any street map. The EPA already publishes it for every census block group in the country in its Smart Location Database.[^epasld] Cities should report it for every proposed subdivision and every comprehensive plan area, alongside density and parking.
- **Set a floor.** The LEED for Neighborhood Development rating system asks projects to be in areas with at least 90 intersections per square mile, or to build internal networks with at least 140.[^leednd] Those numbers make a reasonable starting point for a code. So do maximum block lengths, since a cap of 400 to 600 feet does much of the same work in a way everyone can understand.
- **Require through-connections.** New development should connect to the streets around it and leave stub-outs for future neighbors, and cities should hold the line when the next developer asks to skip connecting.
- **Retrofit where you can.** Existing cul-de-sacs can get walking and cycling cut-throughs to the next street. Aging malls and office parks can be broken into blocks when they're redeveloped. Every new connection shortens someone's trip.
- **Stop approving new pods.** Of everything on this list, this matters most. It's far cheaper to build a connected network the first time than to fix a disconnected one later.

## The takeaway

Most of what we argue about in planning is temporary. Buildings are torn down and replaced. Uses change. Even density drifts over time. The street network is the one decision that tends to outlive everyone who made it. It deserves at least as much scrutiny as the buildings that line it, and right now it gets almost none.

[^ewing2010]: Ewing, R., & Cervero, R. (2010). "Travel and the Built Environment: A Meta-Analysis." *Journal of the American Planning Association*, 76(3), 265–294. [doi.org/10.1080/01944361003766766](https://doi.org/10.1080/01944361003766766)

[^ewing2017]: Ewing, R., & Cervero, R. (2017). "'Does Compact Development Make People Drive Less?' The Answer Is Yes." *Journal of the American Planning Association*, 83(1), 19–25. Table 1 restates the 2010 weighted-average elasticities. [doi.org/10.1080/01944363.2016.1245112](https://doi.org/10.1080/01944363.2016.1245112)

[^marshall2011]: Marshall, W. E., & Garrick, N. W. (2011). "Does Street Network Design Affect Traffic Safety?" *Accident Analysis & Prevention*, 43(3), 769–781. [Summary, University of Notre Dame](https://housingandcommunityregeneration.nd.edu/research/does-street-network-design-affect-traffic-safety/)

[^marshall2010]: Marshall, W. E., & Garrick, N. W. (2010). "Street Network Types and Road Safety: A Study of 24 California Cities." *Urban Design International*, 15(3), 133–147. [doi.org/10.1057/udi.2009.31](https://doi.org/10.1057/udi.2009.31)

[^marshall2014]: Marshall, W. E., Piatkowski, D. P., & Garrick, N. W. (2014). "Community Design, Street Networks, and Public Health." *Journal of Transport & Health*, 1(4), 326–340. [Summary, University of Notre Dame](https://housingandcommunityregeneration.nd.edu/research/community-design-street-networks-and-public-health/)

[^barrington2015]: Barrington-Leigh, C., & Millard-Ball, A. (2015). "A Century of Sprawl in the United States." *Proceedings of the National Academy of Sciences*, 112(27), 8244–8249. [Full paper (PDF)](https://sprawl.research.mcgill.ca/PNAS2015/Barrington-Leigh-Millard-Ball-PNAS2015-with-SI-1504033112.pdf)

[^fha1938]: Federal Housing Administration (1938). *Planning Profitable Neighborhoods*, Technical Bulletin No. 7. Discussed in [Pennsylvania Historical and Museum Commission, "Subdivision Plan/Layout"](https://www.phmc.state.pa.us/portal/communities/pa-suburbs/field-guide/subdivision.html).

[^jacobs1961]: Jacobs, J. (1961). *The Death and Life of Great American Cities*. Random House. Chapter 9, "The Need for Small Blocks."

[^ggwash]: Greater Greater Washington, "Virginia's New Street Connectivity Regulations: The Specifics." [ggwash.org/view/1346](https://ggwash.org/view/amp/1346)

[^bizsense]: Richmond BizSense (2009), "Home Builders Call Cul-de-Sac Rules a Dead End." [richmondbizsense.com](https://richmondbizsense.com/2009/04/02/home-builders-call-cul-de-sac-rules-a-dead-end/)

[^vdot2011]: Virginia Department of Transportation (2011), "Chapter 870: Revision of Secondary Street Acceptance Requirements," presentation to the Commonwealth Transportation Board, October 19, 2011. [PDF](https://ctb.virginia.gov/media/ctb/agendas-and-meeting-minutes/2011/oct/pres/Agenda_Item_9_Ch_870_CTB_Presentation_Oct_19.pdf)

[^epasld]: U.S. Environmental Protection Agency, Smart Location Mapping and the Smart Location Database. [epa.gov/smartgrowth/smart-location-mapping](https://www.epa.gov/smartgrowth/smart-location-mapping)

[^leednd]: U.S. Green Building Council, LEED v4 for Neighborhood Development, "Connected and Open Community" prerequisite. [LEEDuser summary](https://leeduser.buildinggreen.com/credit/ND-v4/NPDp3)

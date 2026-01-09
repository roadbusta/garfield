# Garfield v2 - Product Requirements Document (Front-End Focus)

## Executive Summary

Garfield v2 improves the front-end user experience while keeping the existing data collection and storage architecture. The upgrade focuses on **better visualization** and **basic analytics** using the existing CSV data.

**Target Users**: Family and friends (5-10 trusted users)
**Current State**: Single-user, basic map viewer with date picker and slider
**Vision**: Intuitive, visual pet tracker with playback, analytics, and multi-user access
**Scope**: Front-end only - no backend/database changes, works with existing data/cleaned/locations.csv

---

## Core Principles

1. **No backend changes** - Use existing CSV files from data/cleaned/locations.csv
2. **Streamlit-based** - Keep current tech stack, enhance with better components
3. **Incremental improvements** - Each feature can be built and deployed independently
4. **Mobile-friendly** - Responsive design for phone viewing

---

## 1. User Experience & Interface Improvements

### 1.1 Simple Authentication
**Priority**: High
**User Story**: As a family member, I want to securely access Garfield's location data.

**Requirements**:
- Simple password protection (single shared password for all family members)
- Session persistence (don't re-ask on every page load)
- Login page before accessing app

**Technical Notes**:
- Use streamlit-authenticator with simple password stored in config.yaml
- No database needed - just check password matches
- All family members share one password (can add individual accounts later)

### 1.2 Improved Main Dashboard
**Priority**: High
**User Story**: As a viewer, I want to quickly see where Garfield is and where he's been.

**Current State**: Date picker, slider, basic map

**Proposed Layout**:
```
┌──────────────────────────────────────────────┐
│ 🐈 Where is Garfield?                        │
├──────────────────────────────────────────────┤
│ Last Seen: 2 mins ago • Today: 1.2 km        │
├──────────────────┬───────────────────────────┤
│                  │ Date Picker               │
│                  │ ┌──────────────────────┐  │
│                  │ │ Jan 9, 2026          │  │
│                  │ └──────────────────────┘  │
│                  │                           │
│   Map View       │ ⏯ Play | ⏸ Pause         │
│   (70% width)    │ Speed: [1x][2x][4x][8x]  │
│                  │                           │
│                  │ Timeline Slider           │
│                  │ ━━━━●━━━━━━━━━━━━━        │
│                  │ 8:00 AM                   │
│                  │                           │
│                  │ Today's Path:             │
│                  │ 📍 Home (8:00 AM)         │
│                  │ 📍 Garden (10:30 AM)      │
│                  │ 📍 Home (2:15 PM)         │
└──────────────────┴───────────────────────────┘
```

**Key Features**:
- **Quick stats at top**: Last seen time and today's distance
- **Larger map**: 70% of screen width for better visibility
- **Sidebar controls**: All controls in right panel
- **Location list**: Show key stops during the day below slider
- **Clean, simple layout**: No overwhelming features

### 1.3 Animated Playback ("Play Button")
**Priority**: High
**User Story**: As a viewer, I want to watch Garfield's journey automatically.

**Requirements**:
- Play button that auto-advances the slider
- Speed controls: 1x, 2x, 4x, 8x
- Pause button to stop
- Display current timestamp during playback

**Technical Implementation**:
- Use Streamlit session state + auto-rerun
- On Play: increment slider position, wait based on speed, rerun
- Simple approach: st.session_state.playing = True/False
- Update slider value programmatically

### 1.4 Enhanced Map Features
**Priority**: Medium
**User Story**: As a viewer, I want better visual clarity of Garfield's movements.

**Simple Improvements**:
- **Path coloring**: Different colors for AM vs PM (blue vs orange)
- **Better markers**: Numbered markers (1, 2, 3...) showing order
- **Popup improvements**: Show time + address in popup
- **Start/end markers**: Special icons for first and last position of day
- **Map style toggle**: Switch between Satellite and Street view

---

## 2. Simple Analytics

### 2.1 Basic Stats Page
**Priority**: Medium
**User Story**: As an owner, I want to see patterns in Garfield's movement.

**Simple Analytics** (read from CSV):
```
📊 Analytics
├─ Distance Over Time
│  • Line chart: Daily distance traveled
│  • X-axis: Dates, Y-axis: km
│
├─ Activity by Hour
│  • Bar chart: Number of location updates by hour of day
│  • Shows when Garfield is most active
│
└─ Summary Stats
   • Total distance (all time)
   • Average distance per day
   • Most active hour
   • Days tracked
```

**Technical Details**:
- Read locations.csv with pandas
- Calculate distance between consecutive points (Haversine formula)
- Group by date for daily totals
- Use Streamlit's built-in charts (st.line_chart, st.bar_chart)
- No caching needed - CSV is small enough to load each time


---

## 3. Implementation Plan

### Phase 1: Core UI Improvements (Start Here)
**Estimated effort**: 3-5 hours

1. **Add Simple Authentication**
   - Install streamlit-authenticator
   - Create config.yaml with shared password
   - Add login page

2. **Improve Main Dashboard Layout**
   - Reorganize into sidebar + main map area
   - Add quick stats at top (last seen, today's distance)
   - Make map larger (70% width)
   - Add location list showing key stops

3. **Implement Play Button**
   - Add play/pause buttons
   - Auto-advance slider using session state
   - Add speed controls (1x, 2x, 4x, 8x)

**Files to modify**:
- app/app.py (main changes)
- Create: config.yaml (auth configuration)
- Install: streamlit-authenticator

### Phase 2: Map Enhancements
**Estimated effort**: 2-3 hours

1. **Better Visual Styling**
   - Color paths by time of day (AM=blue, PM=orange)
   - Number markers (1, 2, 3...) to show order
   - Special icons for start/end of day
   - Improve popup content (time + address)

2. **Map Controls**
   - Add map style toggle (Satellite vs Street)
   - Better default zoom level

**Files to modify**:
- app/app.py (map rendering section)

### Phase 3: Basic Analytics
**Estimated effort**: 2-4 hours

1. **Create Analytics Page**
   - Add new page: pages/1_Analytics.py
   - Distance over time (line chart)
   - Activity by hour (bar chart)
   - Summary stats

2. **Helper Functions**
   - Create utils/analytics.py
   - Haversine distance calculator
   - Data aggregation functions

**Files to create**:
- pages/1_Analytics.py
- utils/analytics.py

---

## 4. Success Criteria

**Must Have**:
- ✅ Login page protecting app access
- ✅ Play button that automatically shows Garfield's journey
- ✅ Improved layout with larger map and better controls
- ✅ Quick stats showing last seen and today's distance

**Should Have**:
- ✅ Analytics page with basic charts
- ✅ Better map markers and path styling
- ✅ Map style toggle

**Nice to Have** (future):
- Multi-day/date range view
- Heatmap of favorite locations
- Export functionality
- Mobile app

---

## 5. Technical Notes

**Current Tech Stack** (Keep):
- Streamlit 1.52.2
- Folium 0.20.0
- Pandas 2.3.3
- Python 3.12.9

**Add**:
- streamlit-authenticator (for simple login)
- Custom CSS for layout improvements

**Data Source**:
- Continue using data/cleaned/locations.csv
- Continue using app/locations.csv
- No database migration needed
- Existing processor.py continues to work

**File Structure** (simplified):
```
garfield/
├── app/
│   ├── app.py              # UPDATED: Main dashboard with improvements
│   ├── pages/
│   │   └── 1_Analytics.py  # NEW: Analytics page
│   └── utils/
│       └── analytics.py    # NEW: Helper functions
│
├── data/
│   ├── cleaned/
│   │   └── locations.csv   # Keep existing
│   └── raw/                # Keep existing
│
├── config.yaml             # NEW: Auth configuration
│
└── [all other files unchanged]
```

---

## 6. Appendix: Current System (Reference)

**What works well**:
- 15-minute automated data collection via copy_v2.sh
- Clean CSV data via processor.py
- Basic map visualization with Folium
- Simple, focused UI

**What to improve** (addressed in this PRD):
- No authentication → Add simple login
- Manual slider only → Add play button
- Cramped layout → Redesign with larger map
- No analytics → Add basic stats page
- No visual hierarchy → Add quick stats, location list

---

**Document Version**: 2.0 (Simplified)
**Last Updated**: 2026-01-10
**Owner**: Joe
**Focus**: Front-end UI improvements only
**Status**: Draft - Pending Review

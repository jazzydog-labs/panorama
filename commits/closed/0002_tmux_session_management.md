# Tmux Session Management for Multi-Repo Visualization

## Story
As a developer working across the foundry ecosystem, I would like to have a tmux session that displays all repositories simultaneously in an organized layout, with the ability to quickly open and close this view using simple commands, so that I can efficiently monitor and work with multiple repositories at once.

## Acceptance Criteria
- [x] Create a `pano` command that opens a tmux session with all repos
- [x] Each repository should have its own pane showing its current directory
- [x] The layout should be organized and readable (grid or tiled layout)
- [x] Support for all 12 repositories from loom's repos.yaml
- [x] Create a `pano close` or `pano kill` command to close the session
- [x] The session should be named "panorama" for easy identification
- [x] Each pane should start in the repository's root directory
- [x] Handle cases where repos might not be cloned yet gracefully

## High-Level Design
1. **Command Structure**: Add `pano` command to panorama
2. **Tmux Layout**: Use a tiled or grid layout for 12 repos
3. **Session Management**: Named sessions for easy reference
4. **Error Handling**: Check if repos exist before creating panes
5. **Configuration**: Read repos from loom's config/repos.yaml

## Low-Level Design
1. **Scripts to create**:
   - `scripts/pano.sh` - Main command script
   - `scripts/tmux_layout.py` - Python script to calculate optimal layout

2. **Tmux commands**:
   ```bash
   # Create new session
   tmux new-session -d -s panorama -n repos
   
   # Split windows for each repo
   tmux split-window -h -t panorama:repos
   tmux split-window -v -t panorama:repos
   # ... continue splitting
   
   # Send commands to each pane
   tmux send-keys -t panorama:repos.0 'cd ~/dev/jazzydog-labs/foundry/crucible' C-m
   ```

3. **Layout strategy**:
   - For 12 repos: 4x3 grid or 3x4 grid
   - Use even-horizontal and even-vertical layouts
   - Set pane titles to repo names

4. **Command integration**:
   - Add alias or function to shell profile
   - Support subcommands: `pano` (open), `pano close` (kill session)
   - `pano status` to check if session exists
   - `pano refresh` to reload with updated repo list

## Definition of Done
- [x] `pano` command successfully creates tmux session with all 12 repos
- [x] Each pane displays the correct repository directory
- [x] `pano close` cleanly terminates the session
- [x] Script handles missing repositories gracefully
- [x] Documentation added to README
- [x] Demo script created showing the functionality
- [x] Works on macOS and Linux environments

## Status: COMPLETED ✓
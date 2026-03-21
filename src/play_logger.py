"""Play logger for balance analysis.

Records scene transitions, player actions, and timing data.
Outputs summary to console (print → browser devtools) and
provides data for the ending stats screen.
"""


class PlayLogger:
    """Tracks player behavior for balance analysis."""

    def __init__(self):
        self.scene_frames = {}       # scene_name -> total frames spent
        self.scene_visits = {}       # scene_name -> visit count
        self.weekly_actions = []     # list of {week, action, detail, coins_after}
        self.purchases = []          # list of {week, type, name, cost}
        self.job_counts = {}         # job_name -> times taken
        self.mishap_count_by_week = {}  # week -> mishap count
        self.idle_streaks = []       # list of streak lengths

        # Internal tracking
        self._current_scene = None
        self._scene_enter_frame = 0
        self._consecutive_idles = 0
        self._last_action = None     # for repeat detection
        self._repeat_count = 0
        self._repeat_warnings = []   # (action, count, week)

    def scene_enter(self, scene_name, frame):
        """Call when entering a new scene."""
        # Close previous scene
        if self._current_scene is not None:
            elapsed = frame - self._scene_enter_frame
            self.scene_frames[self._current_scene] = (
                self.scene_frames.get(self._current_scene, 0) + elapsed
            )
        self._current_scene = scene_name
        self._scene_enter_frame = frame
        self.scene_visits[scene_name] = (
            self.scene_visits.get(scene_name, 0) + 1
        )

    def log_turn(self, week, action, detail="", coins_after=0):
        """Record a weekly action (job/idle/defrag)."""
        entry = {
            "week": week,
            "action": action,
            "detail": detail,
            "coins": coins_after,
        }
        self.weekly_actions.append(entry)

        # Job count tracking
        if action == "job":
            self.job_counts[detail] = self.job_counts.get(detail, 0) + 1

        # Idle streak tracking
        if action == "idle":
            self._consecutive_idles += 1
        else:
            if self._consecutive_idles >= 3:
                self.idle_streaks.append(self._consecutive_idles)
            self._consecutive_idles = 0

        # Repeat detection
        action_key = f"{action}:{detail}"
        if action_key == self._last_action:
            self._repeat_count += 1
            if self._repeat_count >= 5:
                self._repeat_warnings.append(
                    (action_key, self._repeat_count, week)
                )
                print(f"[PLAY_LOG] ⚠ 同じ行動を{self._repeat_count}回連続: "
                      f"{action_key} (week {week})")
        else:
            self._last_action = action_key
            self._repeat_count = 1

    def log_mishap(self, week, mishap_name):
        """Record a mishap event."""
        self.mishap_count_by_week[week] = (
            self.mishap_count_by_week.get(week, 0) + 1
        )

    def log_purchase(self, week, purchase_type, name, cost):
        """Record equipment purchase or office upgrade."""
        self.purchases.append({
            "week": week,
            "type": purchase_type,
            "name": name,
            "cost": cost,
        })
        print(f"[PLAY_LOG] 購入: {purchase_type}/{name} ({cost}G) week {week}")

    def print_summary(self):
        """Print full play summary to console (F12 devtools)."""
        print("\n" + "=" * 50)
        print("  PLAY LOG SUMMARY")
        print("=" * 50)

        # Scene time analysis
        print("\n■ シーン滞在時間 (フレーム / 概算秒)")
        total_frames = sum(self.scene_frames.values()) or 1
        sorted_scenes = sorted(
            self.scene_frames.items(), key=lambda x: -x[1]
        )
        for scene, frames in sorted_scenes:
            secs = frames / 30.0
            pct = frames * 100 // total_frames
            visits = self.scene_visits.get(scene, 0)
            avg = frames // visits if visits > 0 else 0
            print(f"  {scene:20s}: {frames:6d}F ({secs:6.1f}s) "
                  f"{pct:3d}% | {visits}回訪問 平均{avg}F/回")

        # Job frequency
        print("\n■ 案件受注回数")
        if self.job_counts:
            for job, cnt in sorted(self.job_counts.items(), key=lambda x: -x[1]):
                print(f"  {job}: {cnt}回")
        else:
            print("  (案件なし)")

        # Action breakdown
        action_types = {}
        for entry in self.weekly_actions:
            a = entry["action"]
            action_types[a] = action_types.get(a, 0) + 1
        print("\n■ 行動タイプ別回数")
        for a, cnt in sorted(action_types.items(), key=lambda x: -x[1]):
            print(f"  {a}: {cnt}回")

        # Idle streaks
        if self.idle_streaks:
            print(f"\n■ サボり連続記録: {self.idle_streaks}")

        # Repeat warnings (potential stuck points)
        if self._repeat_warnings:
            print("\n■ ⚠ 繰り返し検出（詰まりポイント候補）")
            for action, count, week in self._repeat_warnings:
                print(f"  week {week}: {action} を{count}回連続")

        # Purchases timeline
        if self.purchases:
            print("\n■ 購入履歴")
            for p in self.purchases:
                print(f"  week {p['week']}: [{p['type']}] "
                      f"{p['name']} ({p['cost']}G)")

        # Coin progression (sampled every 4 weeks)
        if self.weekly_actions:
            print("\n■ 所持金推移（4週ごと）")
            for entry in self.weekly_actions:
                if entry["week"] % 4 == 0:
                    print(f"  week {entry['week']:3d}: {entry['coins']:6d}G")
            last = self.weekly_actions[-1]
            print(f"  week {last['week']:3d}: {last['coins']:6d}G (最終)")

        print("\n" + "=" * 50)

    def emit_json_summary(self):
        """Print JSON summary with special prefix for JS analytics hook."""
        import json
        stats = self.get_stats_for_ending()
        stats["type"] = "ending"
        print("[PLAY_SUMMARY]" + json.dumps(stats))

    def emit_checkpoint(self, week, coins, office_level, rep_rank):
        """Send checkpoint data at regular intervals for dropout analysis."""
        import json
        stats = self.get_stats_for_ending()
        stats["type"] = "checkpoint"
        stats["week"] = week
        stats["coins"] = coins
        stats["office_level"] = office_level
        stats["rep_rank"] = rep_rank
        print("[PLAY_SUMMARY]" + json.dumps(stats))

    def get_stats_for_ending(self):
        """Return summary dict for ending screen display."""
        total_frames = sum(self.scene_frames.values()) or 1
        total_secs = total_frames / 30.0

        # Most time-consuming scene
        top_scene = max(self.scene_frames, key=self.scene_frames.get) \
            if self.scene_frames else "N/A"
        top_scene_pct = (
            self.scene_frames.get(top_scene, 0) * 100 // total_frames
        )

        # Most taken job
        top_job = max(self.job_counts, key=self.job_counts.get) \
            if self.job_counts else "なし"
        top_job_count = self.job_counts.get(top_job, 0)

        # Action counts
        action_types = {}
        for entry in self.weekly_actions:
            a = entry["action"]
            action_types[a] = action_types.get(a, 0) + 1

        return {
            "total_play_secs": total_secs,
            "total_turns": len(self.weekly_actions),
            "top_scene": top_scene,
            "top_scene_pct": top_scene_pct,
            "top_job": top_job,
            "top_job_count": top_job_count,
            "idle_count": action_types.get("idle", 0),
            "defrag_count": action_types.get("defrag", 0),
            "job_variety": len(self.job_counts),
            "stuck_points": len(self._repeat_warnings),
        }

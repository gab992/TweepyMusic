count = 0
live_loop :osc do
  count += 1
  use_real_time
  a = sync "/osc:127.0.0.1:*/play_this"
  puts a
  set :tweet, a
  use_synth :fm
  if (count == 1) or (a[0] > 0.05)
    set :key, chord(((a[1]+1)*90-30).round(),:major7)
    set :temp, a[2]
    set :drum_amp, a[3]
    set :drum_reps, a[4]
  end
  k1 = get[:key]
  play k1[(((a[2])+1)*100-30).round()], amp:(a[3]+1), attack:(a[4]+1), release:(a[5]+1)*0.2, pan:a[6]
end

live_loop :drum2 do
  use_real_time
  sync :osc
  c = get[:drum_amp]
  if one_in(2)
    sample :drum_cymbal_closed, amp:choose([c+1,(c+1)*0.5,(c+1)*0.25])
  else
    sample choose([:drum_tom_hi_hard,:drum_tom_hi_soft,:drum_tom_lo_hard,:drum_tom_lo_soft,:drum_tom_mid_hard,:drum_tom_mid_soft,:drum_snare_hard,:drum_snare_soft]), amp:choose([c+1,(c+1)*0.5])
  end
  if one_in(2)
    sample :drum_heavy_kick
  end
end

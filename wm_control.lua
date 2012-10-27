-- LUA --  I don't know how to header you.

----------------------------
-- change screen

function get_active_id()
	for line in io.popen("xprop -root"):lines() do
		if line:find("^_NET_ACTIVE_WINDOW") then
			return  line:match("^.*%# (.-),")
		end
	end
end
function maximize_p(id)
	state = nil
	for info_line in io.popen("xwininfo -id " .. id .. " -wm"):lines() do
		if state == 1 then
			if info_line:match(":") then
				state = nil
			else
				if info_line:match("Maximize") then
					return 1
				end
			end			
		end
		if info_line:match("Window state:") then
			state = 1
		end
	end
	return nil
end

function change_screen(id, screen)
		-- TODO  extract the commands into variables
	max_width = io.popen("xwininfo -root"):read("*a"):match("geometry%s*(%d*)x")
	x_offset = tonumber(io.popen("xwininfo -id " .. id):read("*a"):match("Absolute.-X:%s*(%d+)"))
		-- position of center
	center = max_width / 2
		-- maxmized-p
	max_p = maximize_p(id)
		-- relative x pos
	rel_x = x_offset % center
	if (max_p) then
		os.execute("wmctrl -i -r " .. id .. " -b remove,maximized_vert,maximized_horz")
	end
	if screen == 0 then
			-- handle panel
		panel_w = tonumber(io.popen("wmctrl -d"):read("*a"):match("%*.-WA:.-(%d-),"))

		if (rel_x <  panel_w) then rel_x = rel_x + panel_w; print("foo") end
		if ( x_offset < center ) then return nil end
		cmd = "wmctrl -i -r " .. id .. " -e 0," ..	0 + rel_x .. ",-1,-1,-1"
		print("0", cmd)
		os.execute(cmd)
	elseif screen == 1 then
		if ( x_offset > center ) then return nil end
		cmd = "wmctrl -i -r " .. id .. " -e 0," .. center + rel_x .. ",-1,-1,-1"
		print(cmd)
		os.execute(cmd)
	end
	if (max_p) then
		os.execute("wmctrl -i -r " .. id .. " -b add,maximized_vert,maximized_horz")
	end
end


change_screen(get_active_id(), 0)


----------------------------
-- notes 
-- TODO can lua grab control of the mouse and keyboard.
--.-- xev should work but sucks

--
----------------------------

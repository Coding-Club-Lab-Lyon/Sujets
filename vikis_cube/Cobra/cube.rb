require 'colorize'

class Cube
  def initialize(*args)
    case args.size
      when 0
        clear_generation
      when 1
        unless args[0].nil?
          parse(args[0])
        else
          clear_generation
        end
    end
    @colorized = false
    @numberize = true
    @rubic
  end

  def colorize(ok)
    @colorize = ok
  end

  def numberize(ok)
    @numberize = ok
  end

  def parse(file_name)
    if (File.file?(file_name))
      print "File '#{file_name}' exists !\n\n"
    else
      print "File '#{file_name}' doesn't exist...\n\n"
      exit 84
    end
    file = File.open(file_name)
    content = file.read
    file.close
    lines = content.split("\n").map(&:split)
    cube = [lines[0..2]] + lines[3..5].map{ |x| x.each_slice(3).to_a}.transpose + [lines[6..8]]
    tmp = cube[0]
    cube[0] = cube[1]
    cube[1] = cube[2]
    cube[2] = cube[3]
    cube[3] = cube[4]
    cube[4] = tmp
    @rubic = cube
  end

  def clear_generation
    print "No file given. Clear generated map !\n"
    @rubic = Array.new(6) {|i| Array.new(3, Array.new(3, i))}
  end

  def get_rubic
    return @rubic
  end

  def is_resolved
    for i in 0..5
      for y in 0..2
        for x in 0..2
          if @rubic[i][y][x] != (i + 48).chr
            return false
          end
        end
      end
    end
    return true
  end

  def to_s
    res =
    "      %d %d %d \n" % [@rubic[4][0][0], @rubic[4][0][1], @rubic[4][0][2]] +
    "      %d %d %d \n" % [@rubic[4][1][0], @rubic[4][1][1], @rubic[4][1][2]] +
    "      %d %d %d \n" % [@rubic[4][2][0], @rubic[4][2][1], @rubic[4][2][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][0][0], @rubic[0][0][1], @rubic[0][0][2], @rubic[1][0][0], @rubic[1][0][1], @rubic[1][0][2], @rubic[2][0][0], @rubic[2][0][1], @rubic[2][0][2], @rubic[3][0][0], @rubic[3][0][1], @rubic[3][0][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][1][0], @rubic[0][1][1], @rubic[0][1][2], @rubic[1][1][0], @rubic[1][1][1], @rubic[1][1][2], @rubic[2][1][0], @rubic[2][1][1], @rubic[2][1][2], @rubic[3][1][0], @rubic[3][1][1], @rubic[3][1][2]] +
    "%d %d %d %d %d %d %d %d %d %d %d %d \n" % [@rubic[0][2][0], @rubic[0][2][1], @rubic[0][2][2],@rubic[1][2][0], @rubic[1][2][1], @rubic[1][2][2],@rubic[2][2][0], @rubic[2][2][1], @rubic[2][2][2],@rubic[3][2][0], @rubic[3][2][1], @rubic[3][2][2]] +
    "      %d %d %d \n" % [@rubic[5][0][0], @rubic[5][0][1], @rubic[5][0][2]] +
    "      %d %d %d \n" % [@rubic[5][1][0], @rubic[5][1][1], @rubic[5][1][2]] +
    "      %d %d %d \n" % [@rubic[5][2][0], @rubic[5][2][1], @rubic[5][2][2]] + "\n"

    if @colorize
      if @numberize
        vals = Array.new(6) {|x| x.to_s + ' '}
      else
        vals = Array.new(6, "  ")
      end
      res = res.gsub("0 ", vals[0].on_blue)
      res = res.gsub("1 ", vals[1].light_black.on_light_white)
      res = res.gsub("2 ", vals[2].on_green)
      res = res.gsub("3 ", vals[3].on_yellow)
      res = res.gsub("4 ", vals[4].on_red)
      res = res.gsub("5 ", vals[5].on_magenta)
    end
    res
  end

  def rotate_inface(face)
    tmp = Array.new(3) {Array.new(3, 0)}

    for y in 0..2
      for x in 0..2
        tmp[x][3 - y - 1] = @rubic[face][y][x]
      end
    end
    @rubic[face] = tmp
  end

  def f
    tmp = [@rubic[4][2][0], @rubic[4][2][1], @rubic[4][2][2]]

    @rubic[4][2] = [@rubic[0][2][2], @rubic[0][1][2], @rubic[0][0][2]]

    @rubic[0][0][2] = @rubic[5][0][0]
    @rubic[0][1][2] = @rubic[5][0][1]
    @rubic[0][2][2] = @rubic[5][0][2]

    @rubic[5][0] = [@rubic[2][2][0], @rubic[2][1][0], @rubic[2][0][0]]

    @rubic[2][0][0] = tmp[0]
    @rubic[2][1][0] = tmp[1]
    @rubic[2][2][0] = tmp[2]
    rotate_inface(1)
  end

  def fi
    f
    f
    f
  end

  def r
    tmp = [@rubic[4][0][2], @rubic[4][1][2], @rubic[4][2][2]]

    @rubic[4][0][2] = @rubic[1][0][2]
    @rubic[4][1][2] = @rubic[1][1][2]
    @rubic[4][2][2] = @rubic[1][2][2]

    @rubic[1][0][2] = @rubic[5][0][2]
    @rubic[1][1][2] = @rubic[5][1][2]
    @rubic[1][2][2] = @rubic[5][2][2]

    @rubic[5][0][2] = @rubic[3][2][0]
    @rubic[5][1][2] = @rubic[3][1][0]
    @rubic[5][2][2] = @rubic[3][0][0]

    @rubic[3][0][0] = tmp[2]
    @rubic[3][1][0] = tmp[1]
    @rubic[3][2][0] = tmp[0]
    rotate_inface(2)
  end

  def ri
    r
    r
    r
  end

  def b
    tmp = [@rubic[4][0][0], @rubic[4][0][1], @rubic[4][0][2]]

    @rubic[4][0] = [@rubic[2][0][2], @rubic[2][1][2], @rubic[2][2][2]]

    @rubic[2][0][2] = @rubic[5][2][2]
    @rubic[2][1][2] = @rubic[5][2][1]
    @rubic[2][2][2] = @rubic[5][2][0]

    @rubic[5][2] = [@rubic[0][0][0], @rubic[0][1][0], @rubic[0][2][0]]

    @rubic[0][0][0] = tmp[2]
    @rubic[0][1][0] = tmp[1]
    @rubic[0][2][0] = tmp[0]
    rotate_inface(3)
  end

  def bi
    b
    b
    b
  end

  def l
    tmp = [@rubic[4][0][0], @rubic[4][1][0], @rubic[4][2][0]]

    @rubic[4][0][0] = @rubic[3][2][2]
    @rubic[4][1][0] = @rubic[3][1][2]
    @rubic[4][2][0] = @rubic[3][0][2]

    @rubic[3][0][2] = @rubic[5][2][0]
    @rubic[3][1][2] = @rubic[5][1][0]
    @rubic[3][2][2] = @rubic[5][0][0]

    @rubic[5][0][0] = @rubic[1][0][0]
    @rubic[5][1][0] = @rubic[1][1][0]
    @rubic[5][2][0] = @rubic[1][2][0]

    @rubic[1][0][0] = tmp[0]
    @rubic[1][1][0] = tmp[1]
    @rubic[1][2][0] = tmp[2]
    rotate_inface(0)
  end

  def li
    l
    l
    l
  end

  def d
    tmp = [@rubic[0][2][0], @rubic[0][2][1], @rubic[0][2][2]]

    @rubic[0][2] = [@rubic[3][2][0], @rubic[3][2][1], @rubic[3][2][2]]
    @rubic[3][2] = [@rubic[2][2][0], @rubic[2][2][1], @rubic[2][2][2]]
    @rubic[2][2] = [@rubic[1][2][0], @rubic[1][2][1], @rubic[1][2][2]]
    @rubic[1][2] = [tmp[0], tmp[1], tmp[2]]
    rotate_inface(5)
  end

  def di
    d
    d
    d
  end

  def transform_left
    tmp = [@rubic[3][1][0], @rubic[3][1][1], @rubic[3][1][2]]

    @rubic[3][1] = [@rubic[2][1][0], @rubic[2][1][1], @rubic[2][1][2]]
    @rubic[2][1] = [@rubic[1][1][0], @rubic[1][1][1], @rubic[1][1][2]]
    @rubic[1][1] = [@rubic[0][1][0], @rubic[0][1][1], @rubic[0][1][2]]
    @rubic[0][1] = [tmp[0], tmp[1], tmp[2]]
    d
    ui
  end

  def transform_right
    transform_left
    transform_left
    transform_left
  end

  def transform_up
    r
    li

    tmp = [@rubic[4][0][1], @rubic[4][1][1], @rubic[4][2][1]]

    @rubic[4][0][1] = @rubic[1][0][1]
    @rubic[4][1][1] = @rubic[1][1][1]
    @rubic[4][2][1] = @rubic[1][2][1]

    @rubic[1][0][1] = @rubic[5][0][1]
    @rubic[1][1][1] = @rubic[5][1][1]
    @rubic[1][2][1] = @rubic[5][2][1]

    @rubic[5][0][1] = @rubic[3][2][1]
    @rubic[5][1][1] = @rubic[3][1][1]
    @rubic[5][2][1] = @rubic[3][0][1]

    @rubic[3][0][1] = tmp[2]
    @rubic[3][1][1] = tmp[1]
    @rubic[3][2][1] = tmp[0]
  end

  def transform_down
    transform_up
    transform_up
    transform_up
  end
end

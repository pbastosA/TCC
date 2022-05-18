#! /bin/sh
# File: iva.sh
#	Run script iva.scr to start this script
# Set messages on
# set -x
#================================================
# USER AREA -- SUPPLY VALUES
#------------------------------------------------
# CMPs for analysis

# Estrutura da análise de velocidades
# Range de cdps = range(80125,306250,125)
# Quantidade de cdps = 1810

CDP_path="../sintheticDataEngland_CDP.su"

cmp1=80125  cmp6=192625 cmp11=306250
cmp2=102625 cmp7=215125
cmp3=125125 cmp8=237625
cmp4=147625 cmp9=260125
cmp5=170125 cmp10=282625

numCMPs=11
#------------------------------------------------
# File names

indata=$CDP_path    # SU format
outpicks=vpick.txt  # ASCII file

#------------------------------------------------
# display choices

myperc=99   # perc value for plot
plottype=1  # 0 = wiggle plot, 1 = image plot

#------------------------------------------------
# Processing variables

# Semblance variables
nvs=150  # number of velocities
dvs=30   # velocity intervals
fvs=1000 # first velocity

# CVS variables
fc=1000 # first CVS velocity
lc=5000 # last CVS velocity
nc=10   # number of CVS velocities (panels)
XX=11   # ODD number of CMPs to stack into central CVS

#================================================
# HOW SEMBLANCE (VELAN) VELOCITIES ARE COMPUTED

# Last Vel = fvs + (( nvs-1 ) * dvs ) = lvs
#	5000 = 500 + (( 99-1 ) * 45 )
#	3900 = 1200 + (( 100-1 ) * 27 )
# Compute last semblance (velan) velocity
lvs=`bc -l << EOF
$fvs + (( $nvs - 1 ) * $dvs )
EOF`
#Modificado do script original (-END por EOF; END` por EOF`)

#------------------------------------------------
# HOW CVS VELOCITIES ARE COMPUTED

#dc = CVS velocity increment
#dc = ( last CVS vel - first CVS vel ) / ( # CVS - 1 )
#m = CVS plot trace spacing (m = d2, vel units)
#m = ( last CVS vel - first CVS vel ) / ( ( # CVS - 1 ) * XX )

#j=1
#while [ j le nc ]
#do
#  vel = fc + { [( lc - fc ) / ( nc - 1 )] * (j-1) }
#  j = j + 1
#done
#================================================
echo " "
echo " *** INTERACTIVE VELOCITY ANALYSIS ***"
echo " "

#------------------------------------------------
# Remove old files. Open new files
rm -f panel.* picks.* par.* tmp*
> $outpicks   # Write empty file for final picks
> par.cmp     # Write empty file for recording CMP values

#------------------------------------------------
# Get ns, dt, first time from seismic file
nt=`sugethw ns < $indata | sed 1q | sed 's/.*ns=//'`
dt=`sugethw dt < $indata | sed 1q | sed 's/.*dt=//'`
ft=`sugethw delrt < $indata | sed 1q | sed 's/.*delrt=//'`

# Convert dt from header value in microseconds
# to seconds for velocity profile plot
dt=`bc -l << EOF
  scale=6
  $dt / 1000000
EOF`
#Modificado do script original (-END por EOF; END` por EOF`)

# XGRAPH: If "delrt", use it; else use zero
if [ $ft -ne 0 ] ; then
  tstart=`bc -l << EOF
    scale=6
    $ft / 1000
  EOF`
else
  tstart=0.0
fi
#Modificado do script original (-END por EOF; END` por EOF`)

#------------------------------------------------
# Initialize "repick" -- for plotting previous picks on velan
repick=1 # 1=false, 0=true

#------------------------------------------------
# BEGIN IVA LOOP
#------------------------------------------------

i=1
while [ $i -le $numCMPs ]
do
# set variable $picknow to current CMP
  eval picknow=\$cmp$i

  if [ $repick -eq 1 ] ; then
   echo " "
   echo "Preparing CMP $i of $numCMPs for Picking "
   echo "Location is CMP $picknow "
  fi

#------------------------------------------------
# Plot CMP (right)
#------------------------------------------------
  suwind < $indata \
           key=cdp min=$picknow max=$picknow > panel.$picknow
  if [ $repick -eq 1 ] ; then
    if [ $plottype -eq 0 ] ; then
      suxwigb < panel.$picknow xbox=634 ybox=10 wbox=300 \
                hbox=450 title="CMP gather $picknow" \
                label1=" Time (s)" label2="Offset (m)" \
                key=offset perc=$myperc verbose=0 &

    else
      suximage < panel.$picknow xbox=634 ybox=10 wbox=300 \
                hbox=450 title="CMP gather $picknow" \
                label1=" Time (s)" perc=$myperc verbose=0 &
    fi
  else
    if [ $plottype -eq 0 ] ; then
      suxwigb < panel.$picknow xbox=946 ybox=10 wbox=300 \
               hbox=450 title="CMP gather $picknow" \
               label1=" Time (s)" label2="Offset (m)" \
               key=offset perc=$myperc verbose=0 &
    else
      suximage < panel.$picknow xbox=946 ybox=10 wbox=300 \
                hbox=450 title="CMP gather $picknow" \
                label1=" Time (s)" perc=$myperc verbose=0 &
    fi
  fi

#------------------------------------------------
# Constant Velocity Stacks (CVS) (middle-left)
# Make CVS plot for first pick effort.
# If re-picking t-v values, do not make this plot.
#------------------------------------------------

# repick: 1=false, 0=true
  if [ $repick -eq 1 ] ; then

# number of CMPs - 1; for windowing
    X=`expr $XX - 1`

# Window CMPs around central CMP (+/- X/2). Write to tmp0
    k1=`expr $picknow - $X / 2` # Window from CMP to CMP - X/2
    k2=`expr $picknow + $X / 2` # Window from CMP to CMP + X/2
    suwind < $indata key=cdp min=$k1 max=$k2 > tmp0

# Calculate CVS velocity increment
# dc = ( last CVS vel - first CVS vel ) / ( # CVS - 1 )

    dc=`bc -l << EOF
    ( $lc - $fc ) / ( $nc - 1 )
EOF`

#Modificado do script original (-END por EOF; END` por EOF`; EOF` no inicio da linha)

# Calculate trace spacing for CVS plot (m = d2, vel units)
# m = ( last CVS vel - first CVS vel ) / ( ( # CVS - 1 ) * XX )
    m=`bc -l << EOF
    ( $lc - $fc ) / ( ( $nc - 1 ) * $XX )
EOF`
#Modificado do script original (-END por EOF; END` por EOF`; END` no início da linha)

# CVS velocity loop
    j=1
    while [ $j -le $nc ]
    do

      vel=`bc -l << EOF
      $fc + $dc * ( $j - 1 )
EOF`
#Modificado do script original (-END por EOF; END` por EOF`; END` no início da linha)

# uncomment to print CVS velocities to screen
##    echo " vel = $vel"

      sunmo < tmp0 vnmo=$vel verbose=0 |
      sustack >> tmp1

      j=`expr $j + 1`
    done

# Compute lowest velocity for annotating CVS plot
# loV = first CVS velocity - ( ( CMP range - 1 ) / 2 ) * vel inc
    loV=`bc -l << EOF
    $fc - ( $X / 2) * $m
EOF`

suxwigb < tmp1 xbox=322 ybox=10 wbox=300 hbox=450 \
	   title="CMP $picknow Constant Velocity Stacks" \
	   label1=" Time (s)" label2="Velocity (m/s)" \
	   f2=$loV d2=$m verbose=0 \
	   perc=$myperc n2tic=5 cmap=rgb0 &

    fi


#------------------------------------------------
# Picking instructions
#------------------------------------------------
echo " "
echo "Preparing CMP $i of $numCMPs for Picking "
echo "Location is CMP $picknow "
echo " Start CVS CMP = $k1  End CVS CMP = $k2"
echo " "
echo " Use the semblance plot to pick (t,v) pairs."
echo " Type \"s\" when the mouse pointer is where you want a pick."
echo " Be sure your picks increase in time."
echo " To control velocity interpolation, pick a first value"
echo " near zero time and a last value near the last time."
echo " Type \"q\" in the semblance plot when you finish picking."

#------------------------------------------------
# Plot semblance (velan) (left)
#------------------------------------------------

# repick: 1=false, 0=true
  if [ $repick -eq 0 ] ; then
#--- --- --- --- --- --- --- --- --- ---

# Get the number of picks (number of lines) in tmp7 |
# Remove blank spaces preceding the line count.
# Remove file name that was returned from "wc".
# Store line count in "npair" to guide line on velan.

    wc -l tmp7 | sed 's/^ *\(.*\)/\1/' > tmp4
    sed 's/tmp7//' < tmp4 > tmp5
    npair=`sort < tmp5`

#--- --- --- --- --- --- --- --- --- ---

    suvelan < panel.$picknow nv=$nvs dv=$dvs fv=$fvs |
    suximage xbox=10 ybox=10 wbox=300 hbox=450 perc=99 \
             units="semblance" f2=$fvs d2=$dvs n2tic=5 \
             title="Semblance Plot CMP $picknow" cmap=hsv2 \
             label1=" Time (s)" label2="Velocity (m/s)" \
             legend=1 units=Semblance verbose=0 gridcolor=black \
             grid1=solid grid2=solid mpicks=picks.$picknow \
             curve=tmp7 npair=$npair curvecolor=white

  else

    suvelan < panel.$picknow nv=$nvs dv=$dvs fv=$fvs |
    suximage xbox=10 ybox=10 wbox=300 hbox=450 perc=99 \
             units="semblance" f2=$fvs d2=$dvs n2tic=5 \
             title="Semblance Plot CMP $picknow" cmap=hsv2 \
             label1=" Time (s)" label2="Velocity (m/s)" \
             legend=1 units=Semblance verbose=0 gridcolor=black \
             grid1=solid grid2=solid mpicks=picks.$picknow

  fi

#------------------------------------------------
# End first set of plots
#================================================
#------------------------------------------------
# Manage picks (1): Prepare picks for sunmo
#------------------------------------------------

  #sort < picks.$picknow -n |
  #Foi retirado o comando acima do script original
  mkparfile <picks.$picknow string1=tnmo string2=vnmo > par.$i
  echo "cdp=$picknow" >> tmp2
  cat par.$i >> tmp2

#================================================
# Begin second set of plots
#------------------------------------------------
#------------------------------------------------
# Flattened seismic data (NMO) plot (middle-right)
#------------------------------------------------

  sunmo < panel.$picknow par=tmp2 verbose=0 > tmp8
  if [ $plottype -eq 0 ] ; then
    suxwigb < tmp8 xbox=634 ybox=10 wbox=300 hbox=450 \
            title="CMP $picknow after NMO" \
            label1=" Time (s)" label2="Offset (m)" \
            verbose=0 perc=$myperc key=offset &
 
  else
    suximage < tmp8 xbox=634 ybox=10 wbox=300 hbox=450 \
            title="CMP $picknow after NMO" \
            label1=" Time (s)" \
            verbose=0 perc=$myperc &
  fi

#------------------------------------------------
# Stack window (right)
#------------------------------------------------
  j=1
  while [ $j -le 8 ]
  do

# Append stack trace into tmp3 multiple times
    sustack < tmp8 >> tmp3

    j=`expr $j + 1`
  done
  echo "teste0"
  suxwigb < tmp3 xbox=946 ybox=10 wbox=200 hbox=450 \
          title="CMP $picknow repeat stack trace" \
          label1=" Time (s)" d2num=50 key=cdp \
          verbose=0 perc=$myperc &
  
#------------------------------------------------
# Manage picks (2): Prepare picks for vel profile
#------------------------------------------------

  sed < par.$i '
  s/tnmo/xin/
  s/vnmo/yin/
              ' > par.uni.$i
#------------------------------------------------
# Velocity profile (left)
#------------------------------------------------

  unisam nout=$nt fxout=$tstart dxout=$dt \
         par=par.uni.$i method=mono |
  xgraph n=$nt nplot=1 d1=$dt f1=$tstart x2beg=$fvs x2end=$lvs \
         label1=" Time (s)" label2="Velocity (m/s)" \
         title="CMP $picknow Stacking Velocity Function" \
         -geometry 300x450+10+10 -bg white style=seismic \
         grid1=solid grid2=solid linecolor=2 marksize=1 mark=0 \
         titleColor=black axesColor=blue &

#------------------------------------------------
# Dialogue with user: re-pick ?
#------------------------------------------------

  echo " "
  echo " t-v PICKS CMP $picknow"
  echo "----------------------"
  cat picks.$picknow
  echo " "
  echo " Use the velocity profile (left),"
  echo "the NMO-corrected gather (middle-right),"
  echo "and the repeated stack trace (right)"
  echo "to decide whether to re-pick the CMP."
  echo " "
  echo "Picks OK? (y/n) " > /dev/tty
  read response

  rm tmp*
# "n" means re-loop. Otherwise, continue to next CMP.

  case $response in
    n*)
        i=$i
        echo " "
        echo "Repick CMP $picknow. Overlay previous picks."
        repick=0
        cp picks.$picknow tmp7
        ;;
     *)
        echo "$picknow $i" >> par.cmp
        i=`expr $i + 1`
        repick=1
        echo "-- CLOSING CMP $picknow WINDOWS --"
        zap xwigb > tmp6
        zap ximage > tmp6
        zap xgraph > tmp6
        ;;
  esac

done

#------------------------------------------------
# Create velocity output file
#------------------------------------------------


mkparfile < par.cmp string1=cdp string2=# > par.0

i=0
while [ $i -le $numCMPs ]
do
  sed < par.$i 's/$/ \\/g' >> $outpicks
  i=`expr $i + 1`
done

#------------------------------------------------
# Remove files and exit
#------------------------------------------------
echo " "
echo " The output file of t-v pairs is "$outpicks
pause
rm -f panel.* picks.* par.* tmp*
exit
